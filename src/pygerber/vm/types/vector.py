"""`point` module contains `Point` class used to represent 2D coordinates."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, ClassVar

from pygerber.common.namespace import Namespace
from pygerber.vm.types.model import ModelType
from pygerber.vm.types.unit import Unit

if TYPE_CHECKING:
    from typing_extensions import Self


class Vector(ModelType):
    """Represents a point in cartesian coordinate space."""

    x: Unit
    y: Unit

    class unit(Namespace):  # noqa: N801
        """Namespace containing unit vectors."""

        x: ClassVar[Vector]
        y: ClassVar[Vector]
        null: ClassVar[Vector]

    @classmethod
    def from_tuple(cls, data: tuple[float, float]) -> Self:
        """Create a new point from a tuple."""
        return cls(x=Unit.from_float(data[0]), y=Unit.from_float(data[1]))

    @classmethod
    def from_values(cls, x: float, y: float) -> Self:
        """Create a new point from a tuple."""
        return cls(x=Unit.from_float(x), y=Unit.from_float(y))

    @property
    def xy(self) -> tuple[Unit, Unit]:
        """Return point as tuple of Units."""
        return (self.x, self.y)

    def __add__(self, other: object) -> Vector:
        """Add two points."""
        if isinstance(other, Vector):
            return Vector(x=self.x + other.x, y=self.y + other.y)
        if isinstance(other, Unit):
            return Vector(x=self.x + other, y=self.y + other)
        if isinstance(other, (int, float)):
            return Vector(x=self.x + other, y=self.y + other)
        return NotImplemented

    def __sub__(self, other: object) -> Vector:
        """Subtract two points."""
        if isinstance(other, Vector):
            return Vector(x=self.x - other.x, y=self.y - other.y)
        if isinstance(other, Unit):
            return Vector(x=self.x - other, y=self.y - other)
        if isinstance(other, (int, float)):
            return Vector(x=self.x - other, y=self.y - other)
        return NotImplemented

    def __mul__(self, other: object) -> Vector:
        """Multiply two points."""
        if isinstance(other, Vector):
            return Vector(x=self.x * other.x, y=self.y * other.y)
        if isinstance(other, Unit):
            return Vector(x=self.x * other, y=self.y * other)
        if isinstance(other, (int, float)):
            return Vector(x=self.x * other, y=self.y * other)
        return NotImplemented

    def __truediv__(self, other: object) -> Vector:
        """Divide two points."""
        if isinstance(other, Vector):
            return Vector(x=self.x / other.x, y=self.y / other.y)
        if isinstance(other, Unit):
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
        """Calculate clockwise angle between two vectors in degrees clockwise.

        Value returned is always between 0 and 360 (can be 0, never 360).
        """
        return 360 - self.angle_between_cc(other)

    def angle_between_cc(self, other: Vector) -> float:
        """Calculate counter clockwise angle between two vectors in degrees.

        Value returned is always between 0 and 360 (can be 0, never 360).
        """
        v0 = self.normalize()
        v1 = other.normalize()
        angle_radians = math.atan2(
            ((v0.x * v1.y) - (v1.x * v0.y)).value,  # determinant
            ((v0.x * v1.x) + (v0.y * v1.y)).value,  # dot product
        )
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees + (360 * (angle_degrees < 0))

    def normalize(self) -> Vector:
        """Return normalized (unit length) vector."""
        if self.x == 0 and self.y == 0:
            return Vector.from_tuple((1, 0))

        return self / self.length()

    def length(self) -> Unit:
        """Return length of vector."""
        return Unit.from_float(
            math.sqrt((self.x * self.x).value + (self.y * self.y).value)
        )


Vector.unit.x = Vector.from_tuple((1, 0))
Vector.unit.y = Vector.from_tuple((0, 1))
Vector.unit.null = Vector.from_tuple((0, 0))
