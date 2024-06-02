"""PyGerber hight level rendering API version 2.

This API utilizes Parser2 for parsing and SvgRenderer2, RasterRenderer2 for rendering
output files. It is designed to be more limited and easier to use than the previous.
For more advanced uses users will have to fall back to the lower level APIs and
manual interaction with the parser and renderers.
"""

from __future__ import annotations

from pygerber.gerberx3.api._v2 import (
    COLOR_MAP_T,
    DEFAULT_ALPHA_COLOR_MAP,
    DEFAULT_COLOR_MAP,
    GERBER_EXTENSION_TO_FILE_TYPE_MAPPING,
    ColorScheme,
    FileTypeEnum,
    GerberFile,
    GerberFileInfo,
    ImageFormatEnum,
    OnParserErrorEnum,
    ParsedFile,
    ParsedProject,
    PixelFormatEnum,
    Project,
)

__all__ = [
    "COLOR_MAP_T",
    "DEFAULT_ALPHA_COLOR_MAP",
    "DEFAULT_COLOR_MAP",
    "GERBER_EXTENSION_TO_FILE_TYPE_MAPPING",
    "ColorScheme",
    "FileTypeEnum",
    "GerberFile",
    "GerberFileInfo",
    "ImageFormatEnum",
    "OnParserErrorEnum",
    "ParsedFile",
    "ParsedProject",
    "PixelFormatEnum",
    "Project",
]
