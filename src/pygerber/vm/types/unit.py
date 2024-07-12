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
