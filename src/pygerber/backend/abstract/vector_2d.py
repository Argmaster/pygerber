"""Simple of 2D vector container class."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from pygerber.backend.abstract.offset import Offset


class Vector2D(BaseModel):
    """Tuple wrapper for representing size with custom accessors."""

    model_config = ConfigDict(frozen=True)

    x: Offset
    y: Offset

    def as_pixels(self, dpi: int) -> tuple[int, int]:
        """Return size as pixels using given DPI for conversion."""
        return (self.x.as_pixels(dpi), self.y.as_pixels(dpi))

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}(x={self.x}, y={self.y})"
