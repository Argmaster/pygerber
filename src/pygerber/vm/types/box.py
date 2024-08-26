"""`box` module contains definition of `Box` class used to represent 2D boxes."""

from __future__ import annotations

from pydantic import Field

from pygerber.vm.types.model import ModelType
from pygerber.vm.types.vector import Vector


class Box(ModelType):
    """Represents a box in 2D space."""


class AutoBox(Box):
    """Represents a automatically calculated box in 2D space."""

    min_x: float = Field(default=0)
    min_y: float = Field(default=0)
    max_x: float = Field(default=0)
    max_y: float = Field(default=0)


class FixedBox(Box):
    """Represents a fixed box in 2D space.

    Used to specify size and coordinate space of a layer.
    """

    center: Vector
    width: float
    height: float

    @classmethod
    def new(cls, center: tuple[float, float], width: float, height: float) -> FixedBox:
        """Create a new box from a tuple."""
        return cls(center=Vector.from_tuple(center), width=width, height=height)
