"""Module contains implementation details of GerberX3 high level interface of API v2."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, TextIO

from pygerber.gerberx3.api._enums import DEFAULT_COLOR_MAP, FileTypeEnum
from pygerber.gerberx3.ast import State, get_final_state
from pygerber.gerberx3.ast.nodes.attribute.TF import TF_FileFunction
from pygerber.gerberx3.compiler import compile
from pygerber.gerberx3.parser import parse
from pygerber.vm import render
from pygerber.vm.pillow import PillowResult
from pygerber.vm.types.style import Style

if TYPE_CHECKING:
    import PIL.Image

    from pygerber.gerberx3.ast.nodes import File
    from pygerber.vm.rvmc import RVMC

if TYPE_CHECKING:
    from typing_extensions import Self


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
    ) -> PIL.Image.Image:
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
        if self.file_type == FileTypeEnum.INFER_FROM_ATTRIBUTES:
            style = self._get_style_from_file_function()

        if style is None:
            style = DEFAULT_COLOR_MAP[FileTypeEnum.UNDEFINED]

        rvmc = self._get_rvmc()
        result = render(
            rvmc,
            backend="pillow",
            dpmm=dpmm,
        )
        assert isinstance(result, PillowResult)
        return result.get_image(style=style)

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

        return DEFAULT_COLOR_MAP[self.file_type]


@dataclass
class GerberFileInfo:
    """Container for information about Gerber file."""

    min_x_mm: float
    """Minimum X coordinate in file in millimeters."""
    min_y_mm: float
    """Minimum Y coordinate in file in millimeters."""
    max_x_mm: float
    """Maximum X coordinate in file in millimeters."""
    max_y_mm: float
    """Maximum T coordinate in file in millimeters."""

    width_mm: float
    """Width of image in millimeters."""
    height_mm: float
    """Height of image in millimeters."""
