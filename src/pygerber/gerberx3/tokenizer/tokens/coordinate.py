"""Coordinate wrapper class."""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from typing_extensions import Self


class Coordinate(BaseModel):
    """Coordinate wrapper class."""

    coordinate_type: CoordinateType
    sign: CoordinateSign
    offset: str

    @classmethod
    def new(cls, coordinate_type: CoordinateType, offset: str) -> Self:
        """Create new Coordinate object."""
        if len(offset) > 0 and offset[0] in "+-":
            sign = CoordinateSign(offset[0])
            offset = offset[1:].ljust(1, "0")
        else:
            sign = CoordinateSign.Positive

        return cls(coordinate_type=coordinate_type, sign=sign, offset=offset)

    def __str__(self) -> str:
        """Return pretty representation of coordinate token."""
        return f"{self.coordinate_type.value}{self.sign}{self.offset}"


class CoordinateType(Enum):
    """Type of coordinate axis/meaning."""

    X = "X"
    Y = "Y"
    I = "I"  # noqa: E741
    J = "J"
    NULL = ""


class CoordinateSign(Enum):
    """Coordinate sign."""

    Positive = "+"
    Negative = "-"
