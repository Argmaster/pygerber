from __future__ import annotations

from enum import Enum
from typing import Any

import pytest


class Tag(Enum):
    """Enum for all test tags."""

    SHAPELY = "shapely"
    PILLOW = "pillow"
    EXTRAS = "extras"
    LSP = "lsp"
    OPENCV = "opencv"
    SKIMAGE = "skimage"
    SVGLIB = "svglib"
    FORMATTER = "formatter"

    @classmethod
    def _missing_(cls, value: object) -> Any:
        if isinstance(value, str):
            lower = value.lower()
            # Check if value changed to avoid infinite recursion.
            if lower != value:
                for name, member in cls._member_map_.items():
                    if name.lower() == lower:
                        return member

        return super()._missing_(value)


def tag(*tags: Tag) -> pytest.MarkDecorator:
    """Mark test with tags."""
    return pytest.mark.tag(*tags)
