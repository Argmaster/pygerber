"""Utility for loading example Gerber files shipped with PyGerber."""

from __future__ import annotations

from enum import Enum
from pathlib import Path


class ExamplesEnum(Enum):
    """Enumeration of all available examples."""

    UCAMCO_ex_2_Shapes = "ucamco_ex_2_shapes.grb"
    ShapeFlashes = "shape_flashes.grb"


DIRECTORY = Path(__file__).parent


def get_example_path(example: ExamplesEnum) -> Path:
    """Get path to example Gerber file."""
    return DIRECTORY / example.value


def load_example(example: ExamplesEnum) -> str:
    """Load example Gerber file."""
    return get_example_path(example).read_text(encoding="utf-8")
