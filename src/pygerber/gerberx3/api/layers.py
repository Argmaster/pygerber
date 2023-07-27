"""High level API for rendering multi layer gerber projects."""
from __future__ import annotations

from abc import abstractmethod
from pathlib import Path
from typing import Optional

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.backend.abstract.result_handle import ResultHandle
from pygerber.backend.abstract.vector_2d import Vector2D
from pygerber.backend.rasterized_2d.backend_cls import (
    Rasterized2DBackend,
    Rasterized2DBackendOptions,
)
from pygerber.gerberx3.api.color_scheme import ColorScheme
from pygerber.gerberx3.api.errors import RenderingResultNotReadyError
from pygerber.gerberx3.parser.parser import Parser, ParserOnErrorAction, ParserOptions
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer


class Layer:
    """Representation of Gerber X3 image layer."""

    source: Path

    def __init__(
        self,
        source: Path | str,
        *,
        parser_error: ParserOnErrorAction = ParserOnErrorAction.Raise,
    ) -> None:
        """Initialize Layer object."""
        self.source_path = Path(source).expanduser().resolve()
        self.source_content = self.source.read_text(encoding="utf-8")

        self.parser_error = parser_error

        self.tokenizer = self._create_tokenizer()
        self.backend = self._create_backend()
        self.parser = self._create_parser()

        self._rendering_result: Optional[RenderingResult] = None

    def _create_tokenizer(self) -> Tokenizer:
        return Tokenizer()

    @abstractmethod
    def _create_backend(self) -> Backend:
        pass

    @abstractmethod
    def _create_parser(self) -> Parser:
        pass

    def render(self) -> RenderingResult:
        """Render layer image."""
        stack = self.tokenizer.tokenize(self.source_content)
        draw_commands = self.parser.parse(stack)

        result_handle = draw_commands.draw()
        properties = LayerProperties(
            target_bounding_box=self.backend.drawing_target.bounding_box,
            target_coordinate_origin=self.backend.drawing_target.coordinate_origin,
            gerber_bounding_box=self.backend.bounding_box,
            gerber_coordinate_origin=self.backend.coordinate_origin,
        )

        self._rendering_result = RenderingResult(
            result_handle=result_handle,
            properties=properties,
        )
        return self._rendering_result

    def get_rendering_result(self) -> RenderingResult:
        """Return result of rendering Gerber file."""
        if self._rendering_result is None:
            msg = "Use `render()` method to create result first."
            raise RenderingResultNotReadyError(msg)

        return self._rendering_result


class LayerProperties:
    """Properties of layer retrieved from Gerber source code."""

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


class Rasterized2DLayer(Layer):
    """Representation of Gerber X3 rasterized 2D image layer."""

    def __init__(  # noqa: PLR0913
        self,
        source: Path | str,
        *,
        parser_error: ParserOnErrorAction = ParserOnErrorAction.Raise,
        colors: Optional[ColorScheme] = None,
        dpi: int,
        debug_dump_apertures: Optional[Path] = None,
        debug_include_extra_padding: bool = False,
        debug_include_bounding_boxes: bool = False,
    ) -> None:
        """Initialize Layer object."""
        super().__init__(source, parser_error=parser_error)
        self.colors = ColorScheme() if colors is None else colors
        self.dpi = dpi

        self.debug_dump_apertures = debug_dump_apertures
        self.debug_include_extra_padding = debug_include_extra_padding
        self.debug_include_bounding_boxes = debug_include_bounding_boxes

    def _create_backend(self) -> Backend:
        return Rasterized2DBackend(
            Rasterized2DBackendOptions(
                dpi=self.dpi,
                dump_apertures=self.debug_dump_apertures,
                include_debug_padding=self.debug_include_extra_padding,
                include_bounding_boxes=self.debug_include_bounding_boxes,
            ),
        )

    def _create_parser(self) -> Parser:
        return Parser(
            ParserOptions(
                backend=self.backend,
                on_update_drawing_state_error=self.parser_error,
            ),
        )
