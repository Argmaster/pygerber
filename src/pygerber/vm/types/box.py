"""`box` module contains definition of `Box` class used to represent 2D boxes."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pyparsing as pp
from pydantic import Field

from pygerber.vm.types.model import ModelType
from pygerber.vm.types.vector import Vector

if TYPE_CHECKING:
    from typing_extensions import Self


class Box(ModelType):
    """Represents a box in 2D space."""

    min_x: float = Field(default=math.inf)
    min_y: float = Field(default=math.inf)
    max_x: float = Field(default=-math.inf)
    max_y: float = Field(default=-math.inf)

    @classmethod
    def from_vectors(cls, *vectors: Vector) -> Self:
        """Create a box from vectors."""
        assert len(vectors) > 0
        min_x = vectors[0].x
        min_y = vectors[0].y
        max_x = vectors[0].x
        max_y = vectors[0].y

        for vector in vectors[1:]:
            min_x = min(min_x, vector.x)
            min_y = min(min_y, vector.y)
            max_x = max(max_x, vector.x)
            max_y = max(max_y, vector.y)

        return cls(
            min_x=min_x,
            min_y=min_y,
            max_x=max_x,
            max_y=max_y,
        )

    @classmethod
    def from_center_width_height(
        cls, center: tuple[float, float], width: float, height: float
    ) -> Self:
        """Create a box from center, width and height."""
        return cls(
            min_x=center[0] - width / 2,
            min_y=center[1] - height / 2,
            max_x=center[0] + width / 2,
            max_y=center[1] + height / 2,
        )

    @pp.cached_property
    def width(self) -> float:
        """Get width of the box."""
        return abs(self.max_x - self.min_x)

    @pp.cached_property
    def height(self) -> float:
        """Get height of the box."""
        return abs(self.max_y - self.min_y)

    @pp.cached_property
    def center(self) -> Vector:
        """Get mean center of the box."""
        return Vector(
            x=(self.max_x + self.min_x) / 2,
            y=(self.max_y + self.min_y) / 2,
        )

    def __add__(self, other: object) -> Self:
        """Add a vector to the box."""
        if isinstance(other, Box):
            return self.__class__(
                min_x=min(self.min_x, other.min_x),
                min_y=min(self.min_y, other.min_y),
                max_x=max(self.max_x, other.max_x),
                max_y=max(self.max_y, other.max_y),
            )

        if isinstance(other, Vector):
            return self.__class__(
                min_x=self.min_x + other.x,
                min_y=self.min_y + other.y,
                max_x=self.max_x + other.x,
                max_y=self.max_y + other.y,
            )

        return NotImplemented

    def __iadd__(self, other: object) -> Self:
        """Add a vector to the box."""
        return self + other

    def __radd__(self, other: object) -> Self:
        """Add a vector to the box."""
        return self + other

    def __sub__(self, other: object) -> Self:
        """Subtract a vector from the box."""
        if isinstance(other, Vector):
            return self.__class__(
                min_x=self.min_x - other.x,
                min_y=self.min_y - other.y,
                max_x=self.max_x - other.x,
                max_y=self.max_y - other.y,
            )

        return NotImplemented

    def __isub__(self, other: object) -> Self:
        """Subtract a vector from the box."""
        return self - other

    def __rsub__(self, other: object) -> Self:
        """Subtract a vector from the box."""
        return self - other
