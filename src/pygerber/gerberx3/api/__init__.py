"""High level API for rendering Gerber files."""
from __future__ import annotations

from pygerber.common.rgba import RGBA
from pygerber.gerberx3.api.color_scheme import ColorScheme
from pygerber.gerberx3.api.layers import (
    Layer,
    LayerProperties,
    Rasterized2DLayer,
    RenderingResult,
)
from pygerber.gerberx3.parser.parser import ParserOnErrorAction

__all__ = [
    "Layer",
    "ColorScheme",
    "ParserOnErrorAction",
    "Rasterized2DLayer",
    "LayerProperties",
    "RenderingResult",
    "RGBA",
]
