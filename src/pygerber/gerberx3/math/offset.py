"""Offset representation used by drawing backend."""

from __future__ import annotations

import operator
from decimal import Decimal, getcontext
from typing import TYPE_CHECKING, Callable, ClassVar, Sequence

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.state_enums import Unit

if TYPE_CHECKING:
    from typing_extensions import Self

getcontext().prec = 60
INCH_TO_MM_MULTIPLIER = Decimal("25.4")
MM_TO_INCH_MULTIPLIER = Decimal("1") / INCH_TO_MM_MULTIPLIER


class Offset(FrozenGeneralModel):
    """Class representing offset in 2D space."""

    NULL: ClassVar[Offset]

    value: Decimal

    @classmethod
    def new(
        cls,
        value: Decimal | float | str | tuple[int, Sequence[int], int],
        unit: Unit = Unit.Millimeters,
    ) -> Self:
        """Initialize offset with value."""
        # Gerber spec recommends using millimeters as unit, so they are used here too.
        if unit == Unit.Millimeters:
            value = Decimal(value)
        else:
            value = Decimal(value) * INCH_TO_MM_MULTIPLIER

        return cls(value=value)

    @classmethod
    def from_pixels(
        cls,
        value: Decimal | float | str | tuple[int, Sequence[int], int],
        dpi: int,
    ) -> Self:
        """Initialize offset with value."""
        # Gerber spec recommends using millimeters as unit, so they are used here too.
        value = (Decimal(value) / dpi) * INCH_TO_MM_MULTIPLIER
        return cls(value=value)

    def as_millimeters(self) -> Decimal:
        """Offset in millimeters."""
        return self.value

    def as_inches(self) -> Decimal:
        """Offset in millimeters."""
        return self.value * MM_TO_INCH_MULTIPLIER

    def as_unit(self, unit: Unit) -> Decimal:
        """Offset in specified unit."""
        if unit == Unit.Inches:
            return self.as_inches()

        return self.as_millimeters()

    def as_pixels(self, dpi: int | Decimal) -> int:
        """Offset in pixels with respect to drawing DPI."""
        return int(self.as_inches() * dpi)

    def sqrt(self) -> Offset:
        """Return square root of the offset."""
        return Offset(value=self.value.sqrt())

    def _compare(
        self,
        other: object,
        op: Callable,
    ) -> bool:
        if isinstance(other, Offset):
            return op(self.value, other.value)  # type: ignore[no-any-return]
        if isinstance(other, (Decimal, int, float, str)):
            return op(self.value, Decimal(other))  # type: ignore[no-any-return]
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        return self._compare(other, operator.eq)

    def __lt__(self, other: object) -> bool:
        return self._compare(other, operator.lt)

    def __le__(self, other: object) -> bool:
        return self._compare(other, operator.le)

    def __gt__(self, other: object) -> bool:
        return self._compare(other, operator.gt)

    def __ge__(self, other: object) -> bool:
        return self._compare(other, operator.ge)

    def _operator(
        self,
        other: object,
        op: Callable,
    ) -> Offset:
        if isinstance(other, Offset):
            return Offset(value=op(self.value, other.value))
        if isinstance(other, (Decimal, int, float, str)):
            return Offset(value=op(self.value, Decimal(other)))
        return NotImplemented

    def __add__(self, other: object) -> Offset:
        return self._operator(other, operator.add)

    def __sub__(self, other: object) -> Offset:
        return self._operator(other, operator.sub)

    def __mul__(self, other: object) -> Offset:
        return self._operator(other, operator.mul)

    def __truediv__(self, other: object) -> Offset:
        return self._operator(other, operator.truediv)

    def __neg__(self) -> Offset:
        return Offset(value=-self.value)

    def __pow__(self, other: object) -> Offset:
        return self._operator(other, operator.pow)

    def _i_operator(
        self,
        other: object,
        op: Callable,
    ) -> Self:
        if isinstance(other, Offset):
            return self.model_copy(
                update={
                    "value": op(self.value, other.value),
                },
            )
        if isinstance(other, (Decimal, int, float, str)):
            return self.model_copy(
                update={
                    "value": op(self.value, Decimal(other)),
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
        return f"Offset({float(self.value)})"

    __repr__ = __str__


Offset.NULL = Offset(value=Decimal(0))
