"""Module contains implementation details of GerberX3 high level interface of API v2."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, unique
from pathlib import Path
from typing import TYPE_CHECKING, Self, TextIO

from pygerber.backend.rasterized_2d.color_scheme import ColorScheme
from pygerber.gerberx3.parser2.command_buffer2 import ReadonlyCommandBuffer2
from pygerber.gerberx3.parser2.parser2 import (
    Parser2,
    Parser2OnErrorAction,
    Parser2Options,
)
from pygerber.gerberx3.renderer2.raster import (
    ImageFormat,
    PixelFormat,
    RasterFormatOptions,
    RasterRenderer2,
    RasterRenderer2Hooks,
)
from pygerber.gerberx3.renderer2.svg import SvgRenderer2, SvgRenderer2Hooks
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from io import BytesIO


@unique
class OnParserErrorEnum(Enum):
    """Enumeration of possible actions to take on parser error."""

    Ignore = "ignore"
    """Ignore parser errors. Errors which occurred will not be signaled. May yield
    unexpected results for broken files, with missing draw commands or even more
    significant errors."""

    Warn = "warn"
    """Warn on parser error. Parser will log warning message about what went wrong.
    Best for supporting wide range of files without silently ignoring errors in code."""

    Raise = "raise"
    """Raise exception whenever parser encounters error. Will completely break out of
    parsing process, making it impossible to render slightly malformed files."""


@dataclass
class GerberFile:
    """Generic representation of Gerber file.

    This objects provides interface for loading and parsing Gerber files.
    """

    source_code: str

    @classmethod
    def from_file(cls, file_path: str | Path) -> Self:
        """Initialize object with Gerber source code loaded from file on disk."""
        file_path = Path(file_path)
        return cls(file_path.read_text(encoding="utf-8"))

    @classmethod
    def from_str(cls, source_code: str) -> Self:
        """Initialize object with Gerber source code from string."""
        return cls(source_code)

    @classmethod
    def from_buffer(cls, buffer: TextIO) -> Self:
        """Initialize object with Gerber source code from readable buffer."""
        return cls(buffer.read())

    def parse(
        self,
        *,
        on_parser_error: OnParserErrorEnum = OnParserErrorEnum.Ignore,
    ) -> ParsedFile:
        """Parse Gerber file."""
        tokens = Tokenizer().tokenize(self.source_code)
        parser = Parser2(
            Parser2Options(
                on_update_drawing_state_error=Parser2OnErrorAction(
                    on_parser_error.value,
                ),
            ),
        )
        command_buffer = parser.parse(tokens)
        return ParsedFile(
            GerberFileInfo.from_readonly_command_buffer(command_buffer),
            command_buffer,
        )


class ImageFormatEnum(Enum):
    """List of officially supported raster image formats."""

    PNG = "png"
    JPEG = "jpg"
    AUTO = "auto"


class PixelFormatEnum(Enum):
    """List of officially supported pixel formats."""

    RGB = "RGB"
    RGBA = "RGBA"


@dataclass
class ParsedFile:
    """Wrapper around parsed Gerber file.

    This objects allow actions like rendering and retrieving information about file
    contents.
    """

    _info: GerberFileInfo
    _command_buffer: ReadonlyCommandBuffer2

    def get_info(self) -> GerberFileInfo:
        """Get information about Gerber file."""
        return self._info

    def render_svg(
        self,
        destination: BytesIO | Path | str,
        *,
        color_scheme: ColorScheme = ColorScheme.COPPER,
        scale: float = 1.0,
    ) -> None:
        """Render Gerber file to SVG format.

        Parameters
        ----------
        destination : BytesIO | Path | str
            Destination to save file to. When BytesIO is provided, file will be saved
            to buffer. When Path or str is provided, they are treated as file path
            and will be used to open and save file on disk.
        color_scheme : ColorScheme, optional
            Color scheme of image, by default ColorScheme.COPPER
        scale : float, optional
            Scale of image, can be used to scale very large or very small images, by
            default 1.0

        """
        output = SvgRenderer2(
            SvgRenderer2Hooks(color_scheme=color_scheme, scale=Decimal(scale)),
        ).render(self._command_buffer)
        output.save_to(destination)

    def render_raster(
        self,
        destination: BytesIO | Path | str,
        *,
        color_scheme: ColorScheme = ColorScheme.COPPER,
        dpmm: int = 20,
        image_format: ImageFormatEnum = ImageFormatEnum.AUTO,
        pixel_format: PixelFormatEnum = PixelFormatEnum.RGB,
    ) -> None:
        """Render Gerber file to raster image.

        Parameters
        ----------
        destination : BytesIO | Path | str
            Destination to save file to. When BytesIO is provided, file will be saved
            to buffer. When Path or str is provided, they are treated as file path
            and will be used to open and save file on disk.
        color_scheme : ColorScheme, optional
            Color scheme of image, by default ColorScheme.COPPER
        dpmm : int, optional
            Resolution of image in dots per millimeter, by default 96
        image_format : ImageFormatEnum, optional
            Image format to save, by default ImageFormatEnum.AUTO
        pixel_format : PixelFormatEnum, optional
            Pixel format, by default PixelFormatEnum.RGB

        """
        output = RasterRenderer2(
            RasterRenderer2Hooks(color_scheme=color_scheme, dpmm=dpmm),
        ).render(self._command_buffer)
        output.save_to(
            destination,
            RasterFormatOptions(
                image_format=ImageFormat(image_format.value),
                pixel_format=PixelFormat(pixel_format.value),
            ),
        )


@dataclass
class GerberFileInfo:
    """Container for information about Gerber file."""

    min_x_mm: Decimal
    """Minimum X coordinate in file in millimeters."""
    min_y_mm: Decimal
    """Minimum Y coordinate in file in millimeters."""
    max_x_mm: Decimal
    """Maximum X coordinate in file in millimeters."""
    max_y_mm: Decimal
    """Maximum T coordinate in file in millimeters."""

    width_mm: Decimal
    """Width of image in millimeters."""
    height_mm: Decimal
    """Height of image in millimeters."""

    @classmethod
    def from_readonly_command_buffer(cls, buffer: ReadonlyCommandBuffer2) -> Self:
        """Initialize object with information from command buffer."""
        bbox = buffer.get_bounding_box()
        return cls(
            bbox.min_x.as_millimeters(),
            bbox.min_y.as_millimeters(),
            bbox.max_x.as_millimeters(),
            bbox.max_y.as_millimeters(),
            bbox.width.as_millimeters(),
            bbox.height.as_millimeters(),
        )
