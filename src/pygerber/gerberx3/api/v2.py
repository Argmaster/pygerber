"""PyGerber hight level rendering API version 2.

This API utilizes Parser2 for parsing and SvgRenderer2, RasterRenderer2 for rendering
output files. It is designed to be more limited and easier to use than the previous.
For more advanced uses users will have to fall back to the lower level APIs and
manual interaction with the parser and renderers.
"""

from __future__ import annotations

from pygerber.gerberx3.api._v2 import (
    ColorScheme,
    GerberFile,
    GerberFileInfo,
    ImageFormatEnum,
    OnParserErrorEnum,
    ParsedFile,
    PixelFormatEnum,
)

__all__ = [
    "OnParserErrorEnum",
    "GerberFile",
    "ImageFormatEnum",
    "PixelFormatEnum",
    "ParsedFile",
    "GerberFileInfo",
    "ColorScheme",
]
