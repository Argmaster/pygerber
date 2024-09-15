"""`vector` module contains `Vector` class used to represent 2D coordinates."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, ClassVar

from pygerber.common.namespace import Namespace
from pygerber.vm.types.model import ModelType

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.vm.types.matrix import Matrix3x3


class Vector(ModelType):
    """Represents a point in cartesian coordinate space."""

    x: float
    y: float

    class unit(Namespace):  # noqa: N801
        """Namespace containing unit vectors."""

        x: ClassVar[Vector]
        y: ClassVar[Vector]
        null: ClassVar[Vector]

    @classmethod
    def from_tuple(cls, data: tuple[float, float]) -> Self:
        """Create a new point from a tuple."""
        return cls(x=data[0], y=data[1])

    @property
    def xy(self) -> tuple[float, float]:
        """Return point as tuple of Units."""
        return (self.x, self.y)

    def __add__(self, other: object) -> Vector:
        """Add two points."""
        if isinstance(other, Vector):
            return Vector(x=self.x + other.x, y=self.y + other.y)
        if isinstance(other, float):
            return Vector(x=self.x + other, y=self.y + other)
        if isinstance(other, (int, float)):
            return Vector(x=self.x + other, y=self.y + other)
        return NotImplemented

    def __sub__(self, other: object) -> Vector:
        """Subtract two points."""
        if isinstance(other, Vector):
            return Vector(x=self.x - other.x, y=self.y - other.y)
        if isinstance(other, float):
            return Vector(x=self.x - other, y=self.y - other)
        if isinstance(other, (int, float)):
            return Vector(x=self.x - other, y=self.y - other)
        return NotImplemented

    def __mul__(self, other: object) -> Vector:
        """Multiply two points."""
        if isinstance(other, Vector):
            return Vector(x=self.x * other.x, y=self.y * other.y)
        if isinstance(other, float):
            return Vector(x=self.x * other, y=self.y * other)
        if isinstance(other, (int, float)):
            return Vector(x=self.x * other, y=self.y * other)
        return NotImplemented

    def __truediv__(self, other: object) -> Vector:
        """Divide two points."""
        if isinstance(other, Vector):
            return Vector(x=self.x / other.x, y=self.y / other.y)
        if isinstance(other, float):
            return Vector(x=self.x / other, y=self.y / other)
        if isinstance(other, (int, float)):
            return Vector(x=self.x / other, y=self.y / other)
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        """Check if two points are equal."""
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        """Check if point is less than other point."""
        if isinstance(other, Vector):
            return self.x < other.x and self.y < other.y
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        """Check if point is greater than other point."""
        if isinstance(other, Vector):
            return self.x > other.x and self.y > other.y
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        """Check if point is greater than or equal to other point."""
        if isinstance(other, Vector):
            return self.x >= other.x and self.y >= other.y
        return NotImplemented

    def __le__(self, other: object) -> bool:
        """Check if point is less than or equal to other point."""
        if isinstance(other, Vector):
            return self.x <= other.x and self.y <= other.y
        return NotImplemented

    def __neg__(self) -> Vector:
        """Negate vector values."""
        return Vector(x=-self.x, y=-self.y)

    def angle_between(self, other: Vector) -> float:
        """Calculate clockwise angle between two vectors in degrees.

        Value returned is always between 0 and 360 (can be 0, never 360).

        self is the starting vector, other is the ending vector.

        >>> from math import *
        >>> s = Vector(x=sin(pi / 4) * 1, y=-sin(pi / 4) * 1)
        >>> e = Vector(x=-sin(pi / 4) * 1, y=-sin(pi / 4) * 1)
        >>> s.angle_between(e)
        90.0
        >>> e.angle_between(s)
        270.0
        """
        return 360 - self.angle_between_cc(other)

    def angle_between_cc(self, other: Vector) -> float:
        """Calculate counter clockwise angle between two vectors in degrees.

        Value returned is always between 0 and 360 (can be 0, never 360).
        """
        v0 = self.normalized()
        v1 = other.normalized()
        angle_radians = math.atan2(
            ((v0.x * v1.y) - (v1.x * v0.y)),  # determinant
            ((v0.x * v1.x) + (v0.y * v1.y)),  # dot product
        )
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees + (360 * (angle_degrees < 0))

    def normalized(self) -> Vector:
        """Return normalized (unit length) vector."""
        if self.x == 0 and self.y == 0:
            return Vector.from_tuple((1, 0))

        return self / self.length()

    def length(self) -> float:
        """Return length of vector."""
        return math.sqrt((self.x * self.x) + (self.y * self.y))

    def transform(self, matrix: Matrix3x3) -> Vector:
        """Transform vector by matrix."""
        return matrix @ self


Vector.unit.x = Vector.from_tuple((1, 0))
Vector.unit.y = Vector.from_tuple((0, 1))
Vector.unit.null = Vector.from_tuple((0, 0))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
