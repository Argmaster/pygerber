"""`point` module contains `Point` class used to represent 2D coordinates."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.vm.types.model import ModelType
from pygerber.vm.types.unit import Unit

if TYPE_CHECKING:
    from typing_extensions import Self


class Point(ModelType):
    """Represents a point in 2D space."""

    x: Unit
    y: Unit

    @classmethod
    def from_tuple(cls, data: tuple[float, float]) -> Self:
        """Create a new point from a tuple."""
        return cls(x=Unit.from_float(data[0]), y=Unit(value=data[1]))
