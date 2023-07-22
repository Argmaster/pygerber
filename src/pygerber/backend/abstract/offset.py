"""Offset representation used by drawing backend."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, ClassVar, Sequence

from pydantic import BaseModel, ConfigDict

from pygerber.gerberx3.state_enums import Unit

if TYPE_CHECKING:
    from typing_extensions import Self

INCH_TO_MM_MULTIPLIER = Decimal("25.39998628400740663600041656")
MM_TO_INCH_MULTIPLIER = Decimal("0.0393701")


class Offset(BaseModel):
    """Class representing offset in 2D space."""

    model_config = ConfigDict(frozen=True)
    NULL: ClassVar[Offset]

    value: Decimal

    @classmethod
    def new(
        cls,
        value: Decimal | float | str | tuple[int, Sequence[int], int],
        unit: Unit,
    ) -> Self:
        """Initialize offset with value."""
        # Gerber spec recommends using millimeters as unit, so they are used here too.
        if unit == Unit.Millimeters:
            value = Decimal(value)
        else:
            value = Decimal(value) * INCH_TO_MM_MULTIPLIER

        return cls(value=value)

    def as_millimeters(self) -> Decimal:
        """Offset in millimeters."""
        return self.value

    def as_inches(self) -> Decimal:
        """Offset in millimeters."""
        return self.value * MM_TO_INCH_MULTIPLIER

    def as_pixels(self, dpi: int | Decimal) -> int:
        """Offset in pixels with respect to drawing DPI."""
        return round(self.as_inches() * dpi)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Offset):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Offset):
            return NotImplemented
        return self.value < other.value

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Offset):
            return NotImplemented
        return self.value <= other.value

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Offset):
            return NotImplemented
        return self.value > other.value

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Offset):
            return NotImplemented
        return self.value >= other.value

    def __add__(self, other: object) -> Offset:
        if not isinstance(other, Offset):
            return NotImplemented
        return Offset(value=self.value + other.value)

    def __sub__(self, other: object) -> Offset:
        if not isinstance(other, Offset):
            return NotImplemented
        return Offset(value=self.value - other.value)

    def __mul__(self, other: object) -> Offset:
        if not isinstance(other, Offset):
            return NotImplemented
        return Offset(value=self.value * other.value)

    def __truediv__(self, other: object) -> Offset:
        if not isinstance(other, Offset):
            return NotImplemented
        if other.value == 0:
            msg = "Cannot divide by zero offset."
            raise ZeroDivisionError(msg)
        return Offset(value=self.value / other.value)

    def __neg__(self) -> Offset:
        return Offset(value=-self.value)

    def __iadd__(self, other: object) -> Offset:
        """In-place addition."""
        if not isinstance(other, Offset):
            return NotImplemented

        return self.model_copy(
            update={
                "value": self.value + other.value,
            },
        )

    def __isub__(self, other: object) -> Offset:
        """In-place subtraction."""
        if not isinstance(other, Offset):
            return NotImplemented

        return self.model_copy(
            update={
                "value": self.value - other.value,
            },
        )

    def __imul__(self, other: object) -> Offset:
        """In-place multiplication."""
        if not isinstance(other, Offset):
            return NotImplemented

        return self.model_copy(
            update={
                "value": self.value * other.value,
            },
        )

    def __itruediv__(self, other: object) -> Offset:
        """In-place true division."""
        if not isinstance(other, Offset):
            return NotImplemented

        if other.value == 0:
            msg = "Cannot divide by zero offset."
            raise ZeroDivisionError(msg)

        return self.model_copy(
            update={
                "value": self.value / other.value,
            },
        )


Offset.NULL = Offset(value=Decimal(0))
