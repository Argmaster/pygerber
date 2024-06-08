"""Module contains implementation details of GerberX3 high level interface of API v2."""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, unique
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional, TextIO

from PIL import Image

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
    RasterImageRef,
    RasterRenderer2,
    RasterRenderer2Hooks,
)
from pygerber.gerberx3.renderer2.svg import SvgRenderer2, SvgRenderer2Hooks
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from io import BytesIO

    from typing_extensions import Self, TypeAlias


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


@unique
class FileTypeEnum(Enum):
    """Enumeration of possible Gerber file types.

    If file type is not listed here you can request adding it by creating an issue on
    https://github.com/Argmaster/pygerber/issues
    """

    COPPER = "COPPER"
    MASK = "MASK"
    PASTE = "PASTE"
    SILK = "SILK"
    EDGE = "EDGE"

    PLATED = "PLATED"
    NON_PLATED = "NON_PLATED"
    PROFILE = "PROFILE"
    SOLDERMASK = "SOLDERMASK"
    LEGEND = "LEGEND"
    COMPONENT = "COMPONENT"
    GLUE = "GLUE"
    CARBONMASK = "CARBONMASK"
    GOLDMASK = "GOLDMASK"
    HEATSINKMASK = "HEATSINKMASK"
    PEELABLEMASK = "PEELABLEMASK"
    SILVERMASK = "SILVERMASK"
    TINMASK = "TINMASK"
    DEPTHROUT = "DEPTHROUT"
    VCUT = "VCUT"
    VIAFILL = "VIAFILL"
    PADS = "PADS"

    OTHER = "OTHER"
    UNDEFINED = "UNDEFINED"

    INFER_FROM_EXTENSION = "INFER_FROM_EXTENSION"
    INFER_FROM_ATTRIBUTES = "INFER_FROM_ATTRIBUTES"
    INFER = "INFER"

    @classmethod
    def infer_from_attributes(cls, file_function: Optional[str] = None) -> FileTypeEnum:
        """Infer file type from file extension."""
        if file_function is None:
            return cls.UNDEFINED

        function, *_ = file_function.split(",")
        function = function.upper()

        try:
            return FileTypeEnum(function)
        except (ValueError, TypeError, KeyError):
            return cls.UNDEFINED

    @classmethod
    def infer_from_extension(cls, extension: str) -> FileTypeEnum:
        if re.match(r"\.g[0-9]+", extension):
            return FileTypeEnum.COPPER

        if re.match(r"\.gp[0-9]+", extension):
            return FileTypeEnum.COPPER

        if re.match(r"\.gm[0-9]+", extension):
            return FileTypeEnum.COPPER

        return GERBER_EXTENSION_TO_FILE_TYPE_MAPPING.get(
            extension.lower(), FileTypeEnum.UNDEFINED
        )


GERBER_EXTENSION_TO_FILE_TYPE_MAPPING: Dict[str, FileTypeEnum] = {
    ".grb": FileTypeEnum.INFER_FROM_ATTRIBUTES,
    ".gbr": FileTypeEnum.INFER_FROM_ATTRIBUTES,
    ".gto": FileTypeEnum.SILK,
    ".gbo": FileTypeEnum.SILK,
    ".gpt": FileTypeEnum.PADS,
    ".gpb": FileTypeEnum.PADS,
    ".gts": FileTypeEnum.SOLDERMASK,
    ".gbs": FileTypeEnum.SOLDERMASK,
    ".gtl": FileTypeEnum.COPPER,
    ".gbl": FileTypeEnum.COPPER,
    ".gtp": FileTypeEnum.PASTE,
    ".gbp": FileTypeEnum.PASTE,
}


@dataclass
class GerberFile:
    """Generic representation of Gerber file.

    This objects provides interface for loading and parsing Gerber files.
    """

    source_code: str
    file_type: FileTypeEnum

    @classmethod
    def from_file(
        cls,
        file_path: str | Path,
        file_type: FileTypeEnum = FileTypeEnum.UNDEFINED,
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
        file_type: FileTypeEnum = FileTypeEnum.UNDEFINED,
    ) -> Self:
        """Initialize object with Gerber source code from string."""
        if file_type == FileTypeEnum.INFER_FROM_EXTENSION:
            file_type = FileTypeEnum.UNDEFINED
        return cls(source_code, file_type)

    @classmethod
    def from_buffer(
        cls,
        buffer: TextIO,
        file_type: FileTypeEnum = FileTypeEnum.UNDEFINED,
    ) -> Self:
        """Initialize object with Gerber source code from readable buffer."""
        if file_type == FileTypeEnum.INFER_FROM_EXTENSION:
            file_type = FileTypeEnum.UNDEFINED
        return cls(buffer.read(), file_type)

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

        if self.file_type in (FileTypeEnum.INFER_FROM_ATTRIBUTES, FileTypeEnum.INFER):
            file_type = FileTypeEnum.infer_from_attributes(
                parser.context.file_attributes.get(".FileFunction", None)
            )
        else:
            file_type = self.file_type

        return ParsedFile(
            GerberFileInfo.from_readonly_command_buffer(command_buffer),
            command_buffer,
            file_type,
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
    _file_type: FileTypeEnum

    def get_info(self) -> GerberFileInfo:
        """Get information about Gerber file."""
        return self._info

    def get_file_type(self) -> FileTypeEnum:
        """Get type of Gerber file."""
        return self._file_type

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
        quality: int = 85,
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
        quality: int, optional
            Image quality for JPEG format, by default 85.

        """
        output = RasterRenderer2(
            RasterRenderer2Hooks(color_scheme=color_scheme, dpmm=dpmm),
        ).render(self._command_buffer)
        output.save_to(
            destination,
            RasterFormatOptions(
                image_format=ImageFormat(image_format.value),
                pixel_format=PixelFormat(pixel_format.value),
                quality=quality,
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


class Project:
    """Multi file project representation.

    This object can be used to render multiple Gerber files to single image.
    It automatically performs alignment and merging of files.
    Files should be ordered bottom up, topmost layer last, like if adding one layer on
    top of previous.
    """

    def __init__(self, files: List[GerberFile]) -> None:
        self.files = files

    def parse(
        self,
        *,
        on_parser_error: OnParserErrorEnum = OnParserErrorEnum.Ignore,
    ) -> ParsedProject:
        """Parse all Gerber files one by one."""
        return ParsedProject(
            [f.parse(on_parser_error=on_parser_error) for f in self.files],
        )


COLOR_MAP_T: TypeAlias = Dict[FileTypeEnum, ColorScheme]
DEFAULT_COLOR_MAP: COLOR_MAP_T = {
    FileTypeEnum.COPPER: ColorScheme.COPPER,
    FileTypeEnum.MASK: ColorScheme.SOLDER_MASK,
    FileTypeEnum.PASTE: ColorScheme.PASTE_MASK,
    FileTypeEnum.SILK: ColorScheme.SILK,
    FileTypeEnum.EDGE: ColorScheme.SILK,
    FileTypeEnum.OTHER: ColorScheme.DEBUG_1_ALPHA,
    FileTypeEnum.UNDEFINED: ColorScheme.DEBUG_1_ALPHA,
    FileTypeEnum.PLATED: ColorScheme.SOLDER_MASK,
    FileTypeEnum.NON_PLATED: ColorScheme.PASTE_MASK,
    FileTypeEnum.PROFILE: ColorScheme.SILK,
    FileTypeEnum.SOLDERMASK: ColorScheme.SOLDER_MASK,
    FileTypeEnum.LEGEND: ColorScheme.SILK,
    FileTypeEnum.COMPONENT: ColorScheme.PASTE_MASK,
    FileTypeEnum.GLUE: ColorScheme.PASTE_MASK,
    FileTypeEnum.CARBONMASK: ColorScheme.SOLDER_MASK,
    FileTypeEnum.GOLDMASK: ColorScheme.SOLDER_MASK,
    FileTypeEnum.HEATSINKMASK: ColorScheme.SOLDER_MASK,
    FileTypeEnum.PEELABLEMASK: ColorScheme.SOLDER_MASK,
    FileTypeEnum.SILVERMASK: ColorScheme.SOLDER_MASK,
    FileTypeEnum.TINMASK: ColorScheme.SOLDER_MASK,
    FileTypeEnum.DEPTHROUT: ColorScheme.PASTE_MASK,
    FileTypeEnum.VCUT: ColorScheme.PASTE_MASK,
    FileTypeEnum.VIAFILL: ColorScheme.PASTE_MASK,
    FileTypeEnum.PADS: ColorScheme.PASTE_MASK,
}
DEFAULT_ALPHA_COLOR_MAP: COLOR_MAP_T = {
    FileTypeEnum.COPPER: ColorScheme.COPPER_ALPHA,
    FileTypeEnum.MASK: ColorScheme.SOLDER_MASK_ALPHA,
    FileTypeEnum.PASTE: ColorScheme.PASTE_MASK_ALPHA,
    FileTypeEnum.SILK: ColorScheme.SILK_ALPHA,
    FileTypeEnum.EDGE: ColorScheme.SILK_ALPHA,
    FileTypeEnum.OTHER: ColorScheme.DEBUG_1_ALPHA,
    FileTypeEnum.UNDEFINED: ColorScheme.DEBUG_1_ALPHA,
    FileTypeEnum.PLATED: ColorScheme.SOLDER_MASK_ALPHA,
    FileTypeEnum.NON_PLATED: ColorScheme.PASTE_MASK_ALPHA,
    FileTypeEnum.PROFILE: ColorScheme.SILK_ALPHA,
    FileTypeEnum.SOLDERMASK: ColorScheme.SOLDER_MASK_ALPHA,
    FileTypeEnum.LEGEND: ColorScheme.SILK_ALPHA,
    FileTypeEnum.COMPONENT: ColorScheme.PASTE_MASK_ALPHA,
    FileTypeEnum.GLUE: ColorScheme.PASTE_MASK_ALPHA,
    FileTypeEnum.CARBONMASK: ColorScheme.SOLDER_MASK_ALPHA,
    FileTypeEnum.GOLDMASK: ColorScheme.SOLDER_MASK_ALPHA,
    FileTypeEnum.HEATSINKMASK: ColorScheme.SOLDER_MASK_ALPHA,
    FileTypeEnum.PEELABLEMASK: ColorScheme.SOLDER_MASK_ALPHA,
    FileTypeEnum.SILVERMASK: ColorScheme.SOLDER_MASK_ALPHA,
    FileTypeEnum.TINMASK: ColorScheme.SOLDER_MASK_ALPHA,
    FileTypeEnum.DEPTHROUT: ColorScheme.PASTE_MASK_ALPHA,
    FileTypeEnum.VCUT: ColorScheme.PASTE_MASK_ALPHA,
    FileTypeEnum.VIAFILL: ColorScheme.PASTE_MASK_ALPHA,
    FileTypeEnum.PADS: ColorScheme.PASTE_MASK_ALPHA,
}


class ParsedProject:
    """Multi file project representation.

    This object can be used to render multiple Gerber files to single image.
    It automatically performs alignment and merging of files.
    """

    def __init__(self, files: List[ParsedFile]) -> None:
        self.files = files

    def render_raster(
        self,
        destination: BytesIO | Path | str,
        *,
        color_map: COLOR_MAP_T = DEFAULT_COLOR_MAP,
        dpmm: int = 20,
        image_format: ImageFormatEnum = ImageFormatEnum.AUTO,
        pixel_format: PixelFormatEnum = PixelFormatEnum.RGB,
    ) -> None:
        """Render all Gerber file, align them and merge into single file.

        Resulting image will be saved to given `destination`.

        Parameters
        ----------
        destination : BytesIO | Path | str
            Destination to save file to. When BytesIO is provided, file will be saved
            to buffer. When Path or str is provided, they are treated as file path
            and will be used to open and save file on disk.
        color_map : COLOR_MAP_T, optional
            Mapping from image type to color scheme, by default DEFAULT_COLOR_MAP
        dpmm : int, optional
            Resolution of image in dots per millimeter, by default 96
        image_format : ImageFormatEnum, optional
            Image format to save, by default ImageFormatEnum.AUTO
        pixel_format : PixelFormatEnum, optional
            Pixel format, by default PixelFormatEnum.RGB

        """
        if len(self.files) == 0:
            msg = "No files to render"
            raise ValueError(msg)

        min_x_mm = (
            min(
                self.files,
                key=lambda f: f.get_info().min_x_mm,
            )
            .get_info()
            .min_x_mm
        )

        min_y_mm = (
            min(
                self.files,
                key=lambda f: f.get_info().min_y_mm,
            )
            .get_info()
            .min_y_mm
        )

        max_x_mm = (
            max(
                self.files,
                key=lambda f: f.get_info().max_x_mm,
            )
            .get_info()
            .max_x_mm
        )

        max_y_mm = (
            max(
                self.files,
                key=lambda f: f.get_info().max_y_mm,
            )
            .get_info()
            .max_y_mm
        )

        width_mm = max_x_mm - min_x_mm
        height_mm = max_y_mm - min_y_mm

        images = [
            self._render_raster(f, color_map=color_map, dpmm=dpmm) for f in self.files
        ]
        base_image = Image.new(
            "RGBA",
            (
                int(width_mm * dpmm),
                int(height_mm * dpmm),
            ),
            (0, 0, 0, 0),
        )

        for image, file in zip(images, self.files):
            offset_x_mm = abs(min_x_mm - file.get_info().min_x_mm)
            offset_y_mm = abs(max_y_mm - file.get_info().max_y_mm)
            base_image.paste(
                image.image,
                (int(offset_x_mm * dpmm), int(offset_y_mm * dpmm)),
                image.image,
            )

        RasterImageRef(base_image).save_to(
            destination,
            options=RasterFormatOptions(
                image_format=ImageFormat(image_format.value),
                pixel_format=PixelFormat(pixel_format.value),
            ),
        )

    def _render_raster(
        self,
        file: ParsedFile,
        *,
        color_map: COLOR_MAP_T,
        dpmm: int = 20,
    ) -> RasterImageRef:
        output = RasterRenderer2(
            RasterRenderer2Hooks(
                color_scheme=color_map[file.get_file_type()],
                dpmm=dpmm,
            ),
        ).render(
            file._command_buffer,  # noqa: SLF001
        )
        if not isinstance(output, RasterImageRef):
            msg = "Expected RasterImageRef"
            raise TypeError(msg)

        return output
