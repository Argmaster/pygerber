"""Simple of 2D vector container class."""

from __future__ import annotations

import math
import operator
from decimal import Decimal
from typing import TYPE_CHECKING, Callable, ClassVar

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.math.offset import Offset

if TYPE_CHECKING:
    from typing_extensions import Self


class Vector2D(FrozenGeneralModel):
    """Tuple wrapper for representing size with custom accessors."""

    NULL: ClassVar[Vector2D]
    UNIT_X: ClassVar[Vector2D]
    UNIT_Y: ClassVar[Vector2D]

    x: Offset
    y: Offset

    def as_pixels(self, dpi: int) -> tuple[int, int]:
        """Return size as pixels using given DPI for conversion."""
        return (self.x.as_pixels(dpi), self.y.as_pixels(dpi))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector2D):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def _operator(
        self,
        other: object,
        op: Callable,
    ) -> Vector2D:
        if isinstance(other, Offset):
            return Vector2D(
                x=op(self.x, other),
                y=op(self.y, other),
            )
        if isinstance(other, Vector2D):
            return Vector2D(
                x=op(self.x, other.x),
                y=op(self.y, other.y),
            )

        if isinstance(other, (Decimal, int, float, str)):
            return Vector2D(
                x=op(self.x, Decimal(other)),
                y=op(self.y, Decimal(other)),
            )
        return NotImplemented  # type: ignore[unreachable]

    def __add__(self, other: object) -> Vector2D:
        return self._operator(other, operator.add)

    def __sub__(self, other: object) -> Vector2D:
        return self._operator(other, operator.sub)

    def __mul__(self, other: object) -> Vector2D:
        return self._operator(other, operator.mul)

    def __truediv__(self, other: object) -> Vector2D:
        return self._operator(other, operator.truediv)

    def __neg__(self) -> Vector2D:
        return Vector2D(x=-self.x, y=-self.y)

    def _i_operator(
        self,
        other: object,
        op: Callable,
    ) -> Self:
        if isinstance(other, Vector2D):
            return self.model_copy(
                update={
                    "x": op(self.x, other.x),
                    "y": op(self.y, other.y),
                },
            )
        if isinstance(other, Offset):
            return self.model_copy(
                update={
                    "x": op(self.x, other),
                    "y": op(self.y, other),
                },
            )
        if isinstance(other, (Decimal, int, float, str)):
            return self.model_copy(
                update={
                    "x": op(self.x, Decimal(other)),
                    "y": op(self.y, Decimal(other)),
                },
            )
        return NotImplemented  # type: ignore[unreachable]

    def __iadd__(self, other: object) -> Self:
        return self._i_operator(other, operator.add)

    def __isub__(self, other: object) -> Self:
        return self._i_operator(other, operator.sub)

    def __imul__(self, other: object) -> Self:
        return self._i_operator(other, operator.mul)

    def __itruediv__(self, other: object) -> Self:
        return self._i_operator(other, operator.truediv)

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}(x={self.x}, y={self.y})"

    def length(self) -> Offset:
        """Return length of vector."""
        return Offset(value=((self.x * self.x).value + (self.y * self.y).value).sqrt())

    def angle_between_clockwise(self, other: Vector2D) -> float:
        """Calculate angle between two vectors in degrees clockwise."""
        self_norm = self / self.length()
        other_norm = other / other.length()

        dot = other_norm.dot(self_norm)
        determinant = self_norm.determinant(other_norm)

        theta = math.atan2(float(dot.value), float(determinant.value))

        return math.degrees(theta)

    def dot(self, other: Vector2D) -> Offset:
        """Calculate dot product of two vectors."""
        return self.x * other.x + self.y * other.y

    def determinant(self, other: Vector2D) -> Offset:
        """Calculate determinant of matrix constructed from self and other."""
        return self.x * other.y - self.y * other.x


Vector2D.NULL = Vector2D(x=Offset.NULL, y=Offset.NULL)
Vector2D.UNIT_X = Vector2D(x=Offset(value=Decimal(1)), y=Offset.NULL)
Vector2D.UNIT_Y = Vector2D(x=Offset.NULL, y=Offset(value=Decimal(1)))
