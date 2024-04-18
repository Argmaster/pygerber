"""High level API for rendering multi layer gerber projects."""

from __future__ import annotations

from abc import abstractmethod
from io import BytesIO, StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Optional, Union

from pydantic import BaseModel, ConfigDict, model_validator

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.result_handle import ResultHandle
from pygerber.backend.rasterized_2d.backend_cls import (
    Rasterized2DBackend,
    Rasterized2DBackendOptions,
)
from pygerber.backend.rasterized_2d.color_scheme import ColorScheme
from pygerber.backend.rasterized_2d.result_handle import Rasterized2DResultHandle
from pygerber.gerberx3.api._errors import (
    MutuallyExclusiveViolationError,
    RenderingResultNotReadyError,
)
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser.parser import Parser, ParserOnErrorAction, ParserOptions
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer
from pygerber.gerberx3.tokenizer.tokens.bases.token import Token

if TYPE_CHECKING:
    from PIL import Image
    from typing_extensions import Self


class LayerParams(BaseModel):
    """Parameters for Layer object.

    `source_path`, `source_code` and `source_buffer` are mutually exclusive.
    When more than one of them is provided to constructor,
    MutuallyExclusiveViolationError will be raised.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    source_path: Optional[Union[Path, str]] = None
    """Path to source file containing Gerber code. It will be automatically loaded
    from local storage, when provided. Mutually exclusive with `source_code` and
    `source_buffer`.
    """

    source_code: Optional[Union[str, bytes]] = None
    """Gerber source code. Mutually exclusive with `source_path` and `source_buffer`."""

    source_buffer: Optional[Union[StringIO, BytesIO]] = None
    """Buffer containing Gerber source code. Buffer pointer should be at the
    beginning of the buffer. Mutually exclusive with `source_path` and
    `source_code`."""

    parser_error: Union[
        Callable[[Exception, Parser, Token], None],
        ParserOnErrorAction,
    ] = ParserOnErrorAction.Raise
    """Callback function or rule describing how to treat errors during parsing."""

    encoding: str = "utf-8"
    """Encoding of code, used when loading from file, decoding `source_code`
    provided as bytes and reading `source_buffer` provided as BytesIO."""

    draw_region_outlines: bool = False
    """When drawing regions, after filling region, draw also outline of region with
    apertures used for region outlines. This behavior is not expected by KiCAD by
    default but may be useful in some scenarios."""

    @model_validator(mode="after")
    def _load_source_code(self) -> Self:
        """Load source code.

        Raises
        ------
        MutuallyExclusiveViolationError
            When more than one of mutually exclusive `source_path`, `source_code` and
            `source_buffer` is provided to constructor.

        """
        if self.source_path:
            if self.source_code or self.source_buffer:
                msg = "'source_code' and 'source_buffer' provided at once."
                raise MutuallyExclusiveViolationError(msg)

            self.source_code = (
                Path(self.source_path or "source.grb")
                .expanduser()
                .resolve()
                .read_text(encoding=self.encoding)
            )
            return self

        if self.source_code:
            if self.source_path or self.source_buffer:
                msg = "'source_path' and 'source_buffer' provided at once."
                raise MutuallyExclusiveViolationError(msg)

            self.source_code = (
                self.source_code
                if isinstance(self.source_code, str)
                else self.source_code.decode(self.encoding)
            )
            return self

        if self.source_buffer:
            if self.source_path or self.source_code:
                msg = "'source_path' and 'source_buffer' provided at once."
                raise MutuallyExclusiveViolationError(msg)

            source_code = self.source_buffer.read()
            if isinstance(source_code, bytes):
                self.source_code = source_code.decode(encoding="utf-8")
            else:
                self.source_code = source_code

        return self

    def get_source_code(self) -> str:
        """Return source code of layer."""
        if not isinstance(self.source_code, str):
            msg = f"Expected {str} got {type(self.source_code)}."
            raise TypeError(msg)

        return self.source_code


class Layer:
    """Representation of Gerber X3 image layer.

    This is only abstract base class, please use one of its subclasses with rendering
    system guarantees.
    """

    def __init__(self, options: LayerParams) -> None:
        """Create PCB layer.

        Parameters
        ----------
        options: LayerOptions
            Configuration of layer.

        """
        self.options = options

        self.tokenizer = self._create_tokenizer()
        self.backend = self._create_backend()
        self.parser = self._create_parser()

        self._rendering_result: Optional[RenderingResult] = None

    def _create_tokenizer(self) -> Tokenizer:
        return Tokenizer()

    @abstractmethod
    def _create_backend(self) -> Backend:
        pass

    def _create_parser(self) -> Parser:
        return Parser(
            ParserOptions(
                backend=self.backend,
                on_update_drawing_state_error=self.options.parser_error,
            ),
        )

    def render(self) -> RenderingResult:
        """Render layer image."""
        stack = self.tokenizer.tokenize(self.options.get_source_code())
        draw_commands = self.parser.parse(stack)

        result_handle = draw_commands.draw()
        properties = LayerProperties(
            target_bounding_box=self.backend.drawing_target.bounding_box,
            target_coordinate_origin=self.backend.drawing_target.coordinate_origin,
            gerber_bounding_box=self.backend.bounding_box,
            gerber_coordinate_origin=self.backend.coordinate_origin,
        )

        self._rendering_result = self._get_rendering_result_cls()(
            result_handle=result_handle,
            properties=properties,
        )
        return self._rendering_result

    def _get_rendering_result_cls(self) -> type[RenderingResult]:
        return RenderingResult

    def get_rendering_result(self) -> RenderingResult:
        """Return result of rendering Gerber file."""
        if self._rendering_result is None:
            msg = "Use `render()` method to create result first."
            raise RenderingResultNotReadyError(msg)

        return self._rendering_result


class LayerProperties:
    """Properties of layer retrieved from Gerber source code."""

    target_bounding_box: BoundingBox
    """Bounding box of rendering target. May differ from coordinates used in Gerber
    file as it uses rendering target coordinate space."""

    target_coordinate_origin: Vector2D
    """Offset of origin of coordinate system used by rendering target. Bottom left
    corner of coordinate space of rendering target."""

    gerber_bounding_box: BoundingBox
    """Bounding box of drawing area in Gerber file coordinate space."""

    gerber_coordinate_origin: Vector2D
    """Origin of coordinate space of Gerber file. Equivalent to bottom left corner of
    `gerber_bounding_box`.

    Can be useful to determine how to align multiple Gerber files by calculating
    how their coordinate origins are positioned in relation to each other."""

    def __init__(
        self,
        target_bounding_box: BoundingBox,
        target_coordinate_origin: Vector2D,
        gerber_bounding_box: BoundingBox,
        gerber_coordinate_origin: Vector2D,
    ) -> None:
        """Initialize layer properties."""
        self.target_bounding_box = target_bounding_box
        self.target_coordinate_origin = target_coordinate_origin

        self.gerber_bounding_box = gerber_bounding_box
        self.gerber_coordinate_origin = gerber_coordinate_origin


class RenderingResult:
    """Result of rendering of layer."""

    def __init__(
        self,
        properties: LayerProperties,
        result_handle: ResultHandle,
    ) -> None:
        """Initialize rendering result object."""
        self._properties = properties
        self._result_handle = result_handle

    def save(
        self,
        dest: Path | str | BytesIO,
        **options: Any,
    ) -> None:
        """Save result to specified file or buffer.

        Parameters
        ----------
        dest : Path | str | BytesIO
            Write target.
        **options: Any
            Extra parameters which will be passed to saving implementation.
            When dest is BytesIO or alike, `format` option must be specified.
            For Rasterized2D rendering options see [Pillow documentation](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save).

        """
        self._result_handle.save(dest, **options)

    def get_properties(self) -> LayerProperties:
        """Get properties of layer."""
        return self._properties


class Rasterized2DLayerParams(LayerParams):
    """Parameters for Layer with 2D rendering.

    `source_path`, `source_code` and `source_buffer` are mutually exclusive.
    When more than one of them is provided to constructor,
    MutuallyExclusiveViolationError will be raised.
    """

    colors: ColorScheme
    """Colors to use for rendering of image."""

    dpi: int = 1000
    """DPI of output image."""

    debug_dump_apertures: Optional[Path] = None
    """Debug option - dump aperture images to files in given directory."""

    debug_include_extra_padding: bool = False
    """Debug option - include large extra padding on all rendering targets to simplify
    tracking of mispositioned draw commands."""

    debug_include_bounding_boxes: bool = False
    """Debug option - include bounding boxes as square outlines on drawing targets
    to simplify tracking of miscalculated bounding boxes."""


class Rasterized2DLayer(Layer):
    """Representation of Gerber X3 rasterized 2D image layer.

    Rasterized images can be saved in any image format supported by Pillow library.
    For full list of supported formats please refer to
    [Pillow documentation](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).
    """

    options: Rasterized2DLayerParams

    def __init__(self, options: Rasterized2DLayerParams) -> None:
        """Initialize Layer object."""
        if not isinstance(options, Rasterized2DLayerParams):
            msg = f"Expected {Rasterized2DLayerParams} got {type(options)}."  # type: ignore[unreachable]
            raise TypeError(msg)
        super().__init__(options)

    def _create_backend(self) -> Backend:
        return Rasterized2DBackend(
            Rasterized2DBackendOptions(
                dpi=self.options.dpi,
                color_scheme=self.options.colors,
                dump_apertures=self.options.debug_dump_apertures,
                include_debug_padding=self.options.debug_include_extra_padding,
                include_bounding_boxes=self.options.debug_include_bounding_boxes,
                draw_region_outlines=self.options.draw_region_outlines,
            ),
        )

    def _get_rendering_result_cls(self) -> type[RenderingResult]:
        return Rasterized2DRenderingResult


class Rasterized2DRenderingResult(RenderingResult):
    """Result of rendering of layer."""

    _result_handle: Rasterized2DResultHandle

    def get_image(self) -> Image.Image:
        """Get rendered image object."""
        return self._result_handle.get_image()
