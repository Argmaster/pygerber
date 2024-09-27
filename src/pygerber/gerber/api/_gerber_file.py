"""The `_gerber_file` module contains definition of `GerberFile` class."""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, TextIO

import pyparsing as pp

from pygerber.gerber import formatter
from pygerber.gerber.api._enums import (
    COLOR_MAP_T,
    DEFAULT_ALPHA_COLOR_MAP,
    FileTypeEnum,
)
from pygerber.gerber.ast import State, get_final_state
from pygerber.gerber.ast.nodes.attribute.TF import TF_FileFunction
from pygerber.gerber.ast.nodes.enums import UnitMode
from pygerber.gerber.compiler import compile
from pygerber.gerber.parser import parse
from pygerber.vm import render
from pygerber.vm.pillow.vm import PillowResult
from pygerber.vm.types.box import Box
from pygerber.vm.types.style import Style

if TYPE_CHECKING:
    import PIL.Image

    from pygerber.gerber.ast.nodes import File
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

    def __str__(self) -> str:
        return f"""
ImageSpace(
    units = {self.units},
    min_x_mm = {self.min_x_mm},
    min_y_mm = {self.min_y_mm},
    max_x_mm = {self.max_x_mm},
    max_y_mm = {self.max_y_mm},
    dpmm = {self.dpmm},
)
"""


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
        """Initialize object with Gerber source code loaded from file on disk.

        Parameters
        ----------
        file_path : str | Path
            Path to Gerber file on disk.
        file_type : FileTypeEnum, optional
            File type classification, by default FileTypeEnum.INFER

        """
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
        """Initialize GerberFile object with Gerber source code from string.

        Parameters
        ----------
        source_code : str
            Gerber source code as `str`object.
        file_type : FileTypeEnum, optional
            File type classification, by default FileTypeEnum.INFER

        Returns
        -------
        Self
            New instance of GerberFile object.

        """
        if file_type == FileTypeEnum.INFER_FROM_EXTENSION:
            file_type = FileTypeEnum.UNDEFINED
        return cls(source_code, file_type)

    @classmethod
    def from_buffer(
        cls,
        buffer: TextIO,
        file_type: FileTypeEnum = FileTypeEnum.INFER,
    ) -> Self:
        """Initialize object with Gerber source code from readable buffer.

        Parameters
        ----------
        buffer : TextIO
            Readable buffer with Gerber source code.
        file_type : FileTypeEnum, optional
            File type classification, by default FileTypeEnum.INFER

        """
        if file_type == FileTypeEnum.INFER_FROM_EXTENSION:
            file_type = FileTypeEnum.UNDEFINED
        return cls(buffer.read(), file_type)

    def set_parser_options(self, **options: Any) -> Self:
        """Set parser options for this Gerber file.

        This is a window into advanced parser settings, only reason to use this method
        should be for advanced user to tweak parser behavior without binging more
        advanced PyGerber APIs into consideration.

        Parameters
        ----------
        **options : Any
            Parser options.

        Returns
        -------
        Self
            Returns self for method chaining.

        """
        self._flush_cached()
        self._parser_options = options
        return self

    def set_compiler_options(self, **options: Any) -> Self:
        """Set compiler options for this Gerber file.

        This is a window into advanced compiler settings, only
        reason to use this method should be for advanced user to tweak compiler
        behavior without binging more advanced PyGerber APIs into consideration.

        Parameters
        ----------
        **options : Any
            Compiler options.

        Returns
        -------
        Self
            Returns self for method chaining

        """
        self._flush_cached()
        self._compiler_options = options
        return self

    def set_color_map(self, color_map: COLOR_MAP_T) -> Self:
        """Set color map for rendering of this Gerber file.

        Gerber files themselves do not contain color data. Therefore only way to get
        colorful image is to explicitly ask rendering backend to apply particular color
        to image.

        Parameters
        ----------
        color_map : COLOR_MAP_T
            Color map to be used for rendering Gerber file. You can use one of two
            predefined color maps: `DEFAULT_COLOR_MAP` or `DEFAULT_ALPHA_COLOR_MAP` or
            your own. They are both available in `pygerber.gerber.api` module.
            In most basic cases there is no need to alter default color map, as it
            already includes alpha channel thus allows for image stacking.

        Returns
        -------
        Self
            Returns self for method chaining.

        """
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
        """Render Gerber file to raster image using rendering backend based on Pillow
        library.

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

    def format(self, output: TextIO, options: Optional[formatter.Options]) -> None:
        """Format Gerber code and write it to `output` stream."""
        return formatter.format(self._get_ast(), output, options)

    def formats(self, options: Optional[formatter.Options]) -> str:
        """Format Gerber code and return it as `str` object."""
        return formatter.formats(self._get_ast(), options)
