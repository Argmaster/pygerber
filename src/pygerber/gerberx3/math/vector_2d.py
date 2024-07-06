"""Simple of 2D vector container class."""

from __future__ import annotations

import math
import operator
from decimal import Decimal
from typing import TYPE_CHECKING, Callable, ClassVar

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.state_enums import Mirroring, Unit

if TYPE_CHECKING:
    from typing_extensions import Self


class Vector2D(FrozenGeneralModel):
    """Tuple wrapper for representing size with custom accessors."""

    NULL: ClassVar[Vector2D]
    UNIT_X: ClassVar[Vector2D]
    UNIT_Y: ClassVar[Vector2D]

    x: Offset
    y: Offset

    @classmethod
    def new(
        cls,
        x: float | str | Decimal,
        y: float | str | Decimal,
        unit: Unit = Unit.Millimeters,
    ) -> Self:
        """Create new vector with default Offset constructor."""
        return cls(
            x=Offset.new(Decimal(x), unit=unit),
            y=Offset.new(Decimal(y), unit=unit),
        )

    def get_mirrored(self, mirror: Mirroring) -> Self:
        """Get mirrored vector."""
        return self._GET_MIRRORED_DISPATCH_TABLE[mirror](self)

    def _get_mirrored_x(self) -> Self:
        return self.model_copy(
            update={
                "x": -self.x,
            },
        )

    def _get_mirrored_y(self) -> Self:
        return self.model_copy(
            update={
                "y": -self.y,
            },
        )

    def _get_mirrored_xy(self) -> Self:
        return self.model_copy(
            update={
                "x": -self.x,
                "y": -self.y,
            },
        )

    _GET_MIRRORED_DISPATCH_TABLE: ClassVar[dict[Mirroring, Callable[[Self], Self]]] = {
        Mirroring.NoMirroring: lambda s: s,
        Mirroring.X: _get_mirrored_x,
        Mirroring.Y: _get_mirrored_y,
        Mirroring.XY: _get_mirrored_xy,
    }

    def get_rotated(self, angle: float | Decimal) -> Self:
        """Get copy of this vector rotated around (0, 0).

        Angle is in degrees.
        """
        if angle == Decimal("0.0"):
            return self
        return self.rotate_around_origin(angle)

    def get_scaled(self, scale: Decimal) -> Vector2D:
        """Get copy of this vector scaled by factor."""
        if scale == Decimal("1.0"):
            return self
        return self * scale

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
        return NotImplemented

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
        return NotImplemented

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
        """Calculate angle between two vectors in degrees clockwise.

        (Bugged?)
        """
        self_norm = self / self.length()
        other_norm = other / other.length()

        dot = other_norm.dot(self_norm)
        determinant = self_norm.determinant(other_norm)

        theta = math.atan2(float(dot.value), float(determinant.value))

        return math.degrees(theta)

    def angle_between(self, other: Vector2D) -> float:
        """Calculate clockwise angle between two vectors in degrees clockwise.

        Value returned is always between 0 and 360 (can be 0, never 360).
        """
        return 360 - self.angle_between_cc(other)

    def angle_between_cc(self, other: Vector2D) -> float:
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

    def dot(self, other: Vector2D) -> Offset:
        """Calculate dot product of two vectors."""
        return self.x * other.x + self.y * other.y

    def determinant(self, other: Vector2D) -> Offset:
        """Calculate determinant of matrix constructed from self and other."""
        return self.x * other.y - self.y * other.x

    def perpendicular(self) -> Vector2D:
        """Return perpendicular vector to self."""
        return Vector2D(x=self.y, y=-self.x)

    def normalize(self) -> Vector2D:
        """Return normalized (unit length) vector."""
        if self == Vector2D.NULL:
            return Vector2D.UNIT_X

        return self / self.length()

    def as_float_tuple(self) -> tuple[float, float]:
        """Return x, y Offset as tuple."""
        return (float(self.x.value), float(self.y.value))

    def rotate_around_origin(self, angle_degrees: float | Decimal) -> Self:
        """Return vector rotated x degrees around origin."""
        angle_radians = math.radians(angle_degrees)
        return self.__class__(
            x=self.x * math.cos(angle_radians) - self.y * math.sin(angle_radians),
            y=self.x * math.sin(angle_radians) + self.y * math.cos(angle_radians),
        )


Vector2D.NULL = Vector2D(x=Offset.NULL, y=Offset.NULL)
Vector2D.UNIT_X = Vector2D(x=Offset(value=Decimal(1)), y=Offset.NULL)
Vector2D.UNIT_Y = Vector2D(x=Offset.NULL, y=Offset(value=Decimal(1)))
