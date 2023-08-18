"""`pygerber.gerberx3.api` module provides simple, high-level API for rendering
Gerber X3/X2 files.

!!! info "Supported features"

    For list of supported Gerber format features please see
    [Gerber features support](../../../../README.md#gerber-features-support) section.

!!! info "Tutorial"

    For tutorial on how to use high level API see
    [Gerber X3 High Level API](../../../../gerber/high_level_api.md#gerber-x3-high-level-api)
    section.
"""  # noqa: E501
from __future__ import annotations

from pygerber.backend.rasterized_2d.color_scheme import ColorScheme
from pygerber.common.rgba import RGBA
from pygerber.gerberx3.api._errors import (
    GerberX3APIError,
    MutuallyExclusiveViolationError,
    RenderingResultNotReadyError,
)
from pygerber.gerberx3.api._layers import (
    Layer,
    LayerParams,
    LayerProperties,
    Rasterized2DLayer,
    Rasterized2DLayerParams,
    RenderingResult,
)
from pygerber.gerberx3.parser.errors import (
    ApertureNotDefinedError,
    ApertureNotSelectedError,
    CoordinateFormatNotSetError,
    ExitParsingProcessInterrupt,
    IncrementalCoordinatesNotSupportedError,
    InvalidCoordinateLengthError,
    OnUpdateDrawingStateError,
    ParserError,
    ParserFatalError,
    UnitNotSetError,
    UnsupportedCoordinateTypeError,
    ZeroOmissionNotSupportedError,
)
from pygerber.gerberx3.parser.parser import ParserOnErrorAction

__all__ = [
    "RGBA",
    "ColorScheme",
    "Layer",
    "LayerParams",
    "Rasterized2DLayer",
    "Rasterized2DLayerParams",
    "LayerProperties",
    "RenderingResult",
    "ParserOnErrorAction",
    "GerberX3APIError",
    "RenderingResultNotReadyError",
    "MutuallyExclusiveViolationError",
    "ParserError",
    "ZeroOmissionNotSupportedError",
    "IncrementalCoordinatesNotSupportedError",
    "UnsupportedCoordinateTypeError",
    "InvalidCoordinateLengthError",
    "ParserFatalError",
    "OnUpdateDrawingStateError",
    "UnitNotSetError",
    "ApertureNotDefinedError",
    "CoordinateFormatNotSetError",
    "ApertureNotSelectedError",
    "ExitParsingProcessInterrupt",
]
