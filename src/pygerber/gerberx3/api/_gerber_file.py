"""Module contains implementation details of GerberX3 high level interface of API v2."""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, TextIO

import pyparsing as pp

from pygerber.gerberx3.api._enums import (
    COLOR_MAP_T,
    DEFAULT_ALPHA_COLOR_MAP,
    FileTypeEnum,
)
from pygerber.gerberx3.ast import State, get_final_state
from pygerber.gerberx3.ast.nodes.attribute.TF import TF_FileFunction
from pygerber.gerberx3.ast.nodes.enums import UnitMode
from pygerber.gerberx3.compiler import compile
from pygerber.gerberx3.parser import parse
from pygerber.vm import render
from pygerber.vm.pillow.vm import PillowResult
from pygerber.vm.types.box import Box
from pygerber.vm.types.style import Style

if TYPE_CHECKING:
    import PIL.Image

    from pygerber.gerberx3.ast.nodes import File
    from pygerber.vm.rvmc import RVMC

if TYPE_CHECKING:
    from typing_extensions import Self


class Units(Enum):
    """The `Units` enum contains possible Gerber file units."""

    Millimeters = "MM"
    Inches = "IN"


class ImageSpace:
    """Container for information about Gerber image space."""

    def __init__(self, units: UnitMode, box: Box, dpmm: int) -> None:
        self._units = Units(units.value)
        self._min_x = box.min_x
        self._min_y = box.min_y
        self._max_x = box.max_x
        self._max_y = box.max_y
        self._dpmm = dpmm

    @property
    def units(self) -> Units:
        """Units of image space."""
        return self._units

    @property
    def min_x(self) -> float:
        """Minimum X coordinate in image in file defined unit."""
        return self._min_x

    @property
    def min_y(self) -> float:
        """Minimum Y coordinate in image in file defined unit."""
        return self._min_y

    @property
    def max_x(self) -> float:
        """Maximum X coordinate in image in file defined unit."""
        return self._max_x

    @property
    def max_y(self) -> float:
        """Maximum T coordinate in image in file defined unit."""
        return self._max_y

    @property
    def dpmm(self) -> int:
        """Resolution of image in dots per millimeter."""
        return self._dpmm

    @pp.cached_property
    def min_x_mm(self) -> float:
        """Minimum X coordinate of image in millimeters."""
        return self.min_x if self.units == Units.Millimeters else self.min_x * 25.4

    @pp.cached_property
    def min_y_mm(self) -> float:
        """Minimum Y coordinate of image in millimeters."""
        return self.min_y if self.units == Units.Millimeters else self.min_y * 25.4

    @pp.cached_property
    def max_x_mm(self) -> float:
        """Maximum X coordinate of image in millimeters."""
        return self.max_x if self.units == Units.Millimeters else self.max_x * 25.4

    @pp.cached_property
    def max_y_mm(self) -> float:
        """Maximum Y coordinate of image in millimeters."""
        return self.max_y if self.units == Units.Millimeters else self.max_y * 25.4

    @pp.cached_property
    def width_mm(self) -> float:
        """Width of image in millimeters."""
        return self.max_x_mm - self.min_x_mm

    @pp.cached_property
    def height_mm(self) -> float:
        """Height of image in millimeters."""
        return self.max_y_mm - self.min_y_mm

    @pp.cached_property
    def center_x_mm(self) -> float:
        """Center X coordinate of image in millimeters.

        This value can be negative.
        """
        return (self.min_x_mm + self.max_x_mm) / 2

    @pp.cached_property
    def center_y_mm(self) -> float:
        """Center Y coordinate of image in millimeters.

        This value can be negative.
        """
        return (self.min_y_mm + self.max_y_mm) / 2

    @pp.cached_property
    def min_x_pixels(self) -> int:
        """Minimum X coordinate of image in pixels.

        This value can be negative.
        """
        return int(self.min_x_mm * self.dpmm)

    @pp.cached_property
    def min_y_pixels(self) -> int:
        """Minimum Y coordinate of image in pixels.

        This value can be negative.
        """
        return int(self.min_y_mm * self.dpmm)

    @pp.cached_property
    def max_x_pixels(self) -> int:
        """Maximum X coordinate of image in pixels."""
        return int(self.max_x_mm * self.dpmm)

    @pp.cached_property
    def max_y_pixels(self) -> int:
        """Maximum Y coordinate of image in pixels."""
        return int(self.max_y_mm * self.dpmm)


class Image:
    """The `Image` class is a base class for all rendered images returned by
    `GerberFile.render_with_*` methods.
    """

    def __init__(self, image_space: ImageSpace) -> None:
        self._image_space = image_space

    def get_image_space(self) -> ImageSpace:
        """Get information about image space."""
        return self._image_space


class PillowImage(Image):
    """The `PillowImage` class is a rendered image returned by
    `GerberFile.render_with_pillow` method.
    """

    def __init__(self, image_space: ImageSpace, image: PIL.Image.Image) -> None:
        super().__init__(image_space=image_space)
        self._image = image

    def get_image(self) -> PIL.Image.Image:
        """Get image object."""
        return self._image


class GerberFile:
    """Generic representation of Gerber file.

    This objects provides interface for loading and parsing Gerber files.
    """

    def __init__(self, source_code: str, file_type: FileTypeEnum) -> None:
        self.source_code = source_code
        self.file_type = file_type
        self._parser_options: dict[str, Any] = {}
        self._compiler_options: dict[str, Any] = {}
        self._cached_ast: Optional[File] = None
        self._cached_rvmc: Optional[RVMC] = None
        self._cached_final_state: Optional[State] = None
        self._color_map = DEFAULT_ALPHA_COLOR_MAP

    def _flush_cached(self) -> None:
        self._cached_ast = None
        self._cached_rvmc = None
        self._cached_final_state = None

    @classmethod
    def from_file(
        cls,
        file_path: str | Path,
        file_type: FileTypeEnum = FileTypeEnum.INFER,
    ) -> Self:
        """Initialize object with Gerber source code loaded from file on disk."""
        file_path = Path(file_path)
        if file_type == FileTypeEnum.INFER_FROM_EXTENSION:
            file_type = FileTypeEnum.infer_from_extension(file_path.suffix)

        if file_type == FileTypeEnum.INFER:
            file_type = FileTypeEnum.infer_from_extension(file_path.suffix)
            if file_type == FileTypeEnum.UNDEFINED:
                file_type = FileTypeEnum.INFER_FROM_ATTRIBUTES

        return cls(file_path.read_text(encoding="utf-8"), file_type)

    @classmethod
    def from_str(
        cls,
        source_code: str,
        file_type: FileTypeEnum = FileTypeEnum.INFER,
    ) -> Self:
        """Initialize object with Gerber source code from string."""
        if file_type == FileTypeEnum.INFER_FROM_EXTENSION:
            file_type = FileTypeEnum.UNDEFINED
        return cls(source_code, file_type)

    @classmethod
    def from_buffer(
        cls,
        buffer: TextIO,
        file_type: FileTypeEnum = FileTypeEnum.INFER,
    ) -> Self:
        """Initialize object with Gerber source code from readable buffer."""
        if file_type == FileTypeEnum.INFER_FROM_EXTENSION:
            file_type = FileTypeEnum.UNDEFINED
        return cls(buffer.read(), file_type)

    def set_parser_options(self, **options: Any) -> Self:
        """Set parser options for this Gerber file."""
        self._flush_cached()
        self._parser_options = options
        return self

    def set_compiler_options(self, **options: Any) -> Self:
        """Set compiler options for this Gerber file."""
        self._flush_cached()
        self._compiler_options = options
        return self

    def set_color_map(self, color_map: COLOR_MAP_T) -> Self:
        """Set color map for this Gerber file."""
        self._color_map = color_map
        return self

    def _get_final_state(self) -> State:
        if self._cached_final_state is None:
            self._cached_final_state = get_final_state(self._get_ast())

        return self._cached_final_state

    def _get_ast(self) -> File:
        if self._cached_ast is None:
            self._cached_ast = parse(self.source_code, **self._parser_options)

        assert self._cached_ast is not None
        return self._cached_ast

    def _get_rvmc(self) -> RVMC:
        ast = self._get_ast()

        if self._cached_rvmc is None:
            self._cached_rvmc = compile(ast, **self._compiler_options)

        assert self._cached_rvmc is not None
        return self._cached_rvmc

    def render_with_pillow(
        self,
        style: Optional[Style] = None,
        dpmm: int = 20,
    ) -> PillowImage:
        """Render Gerber file to raster image.

        Parameters
        ----------
        style : Style, optional
            Style (color scheme) of rendered image, if value is None, style will be
            inferred from file_type if it possible to determine file_type
            (for FileTypeEnum.INFER*) or specific file_type was specified in
            constructor, by default None
        dpmm : int, optional
            Resolution of image in dots per millimeter, by default 20

        """
        if self.file_type in (FileTypeEnum.INFER_FROM_ATTRIBUTES, FileTypeEnum.INFER):
            style = self._get_style_from_file_function()

        if style is None:
            style = self._color_map[self.file_type]

        rvmc = self._get_rvmc()
        result = render(
            rvmc,
            backend="pillow",
            dpmm=dpmm,
        )
        assert isinstance(result, PillowResult)
        return PillowImage(
            image_space=ImageSpace(
                units=self._get_final_state().unit_mode,
                box=result.main_box,
                dpmm=dpmm,
            ),
            image=result.get_image(style=style),
        )

    def _get_style_from_file_function(self) -> Style:
        file_function_node = self._get_final_state().attributes.file_attributes.get(
            ".FileFunction"
        )
        if file_function_node is None:
            self.file_type = FileTypeEnum.UNDEFINED

        else:
            assert isinstance(file_function_node, TF_FileFunction)
            self.file_type = FileTypeEnum.infer_from_attributes(
                file_function_node.file_function.value
            )

        return self._color_map[self.file_type]