"""`unit` module contains `Unit` class used to represent distances."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.vm.types.model import ModelType

if TYPE_CHECKING:
    from typing_extensions import Self


class Unit(ModelType):
    """Unit used to represent distances in 2D space used by virtual machines."""

    value: float = 0

    @classmethod
    def from_float(cls, value: float) -> Self:
        """Create a new unit from a float."""
        return cls(value=value)

    def __add__(self, other: object) -> Unit:
        """Add two units."""
        if isinstance(other, Unit):
            return Unit(value=self.value + other.value)
        if isinstance(other, (int, float)):
            return Unit(value=self.value + other)
        return NotImplemented

    def __sub__(self, other: object) -> Unit:
        """Subtract two units."""
        if isinstance(other, Unit):
            return Unit(value=self.value - other.value)
        if isinstance(other, (int, float)):
            return Unit(value=self.value - other)
        return NotImplemented

    def __mul__(self, other: object) -> Unit:
        """Multiply two units."""
        if isinstance(other, Unit):
            return Unit(value=self.value * other.value)
        if isinstance(other, (int, float)):
            return Unit(value=self.value * other)
        return NotImplemented

    def __truediv__(self, other: object) -> Unit:
        """Divide two units."""
        if isinstance(other, Unit):
            return Unit(value=self.value / other.value)
        if isinstance(other, (int, float)):
            return Unit(value=self.value / other)
        return NotImplemented

    def __eq__(self, value: object) -> bool:
        """Check if two unit instances are equal."""
        if isinstance(value, Unit):
            return self.value == value.value

        if isinstance(value, (int, float)):
            return self.value == value

        return NotImplemented

    def __lt__(self, value: object) -> bool:
        """Check if unit is less than other unit."""
        if isinstance(value, Unit):
            return self.value < value.value

        if isinstance(value, (int, float)):
            return self.value < value

        return NotImplemented

    def __gt__(self, value: object) -> bool:
        """Check if unit is greater than other unit."""
        if isinstance(value, Unit):
            return self.value > value.value

        if isinstance(value, (int, float)):
            return self.value > value

        return NotImplemented

    def __le__(self, value: object) -> bool:
        """Check if unit is less than or equal to other unit."""
        if isinstance(value, Unit):
            return self.value <= value.value

        if isinstance(value, (int, float)):
            return self.value <= value

        return NotImplemented

    def __ge__(self, value: object) -> bool:
        """Check if unit is greater than or equal to other unit."""
        if isinstance(value, Unit):
            return self.value >= value.value

        if isinstance(value, (int, float)):
            return self.value >= value

        return NotImplemented

    def __neg__(self) -> Unit:
        """Negate the unit."""
        return Unit(value=-self.value)
