"""`box` module contains definition of `Box` class used to represent 2D boxes."""

from __future__ import annotations

from pygerber.vm.types.model import ModelType
from pygerber.vm.types.point import Point


class Box(ModelType):
    """Represents a box in 2D space.

    Used to specify size and coordinate space of a layer.
    """

    center: Point
    width: float
    height: float

    @classmethod
    def new(cls, center: tuple[float, float], width: float, height: float) -> Box:
        """Create a new box from a tuple."""
        return cls(center=Point.from_tuple(center), width=width, height=height)
