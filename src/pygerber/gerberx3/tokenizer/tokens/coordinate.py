"""Coordinate wrapper class."""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Optional

from pygerber.common.frozen_general_model import FrozenGeneralModel

if TYPE_CHECKING:
    from typing_extensions import Self


class Coordinate(FrozenGeneralModel):
    """Coordinate wrapper class."""

    coordinate_type: CoordinateType
    sign: CoordinateSign
    offset: str

    @classmethod
    def new(cls, coordinate_type: CoordinateType, offset: Optional[str]) -> Self:
        """Create new Coordinate object."""
        if offset is None:
            coordinate_type = coordinate_type.to_missing()
            offset = ""
            sign = CoordinateSign.Positive

        elif len(offset) > 0 and offset[0] in "+-":
            sign = CoordinateSign(offset[0])
            offset = offset[1:].ljust(1, "0")

        else:
            sign = CoordinateSign.Positive

        return cls(coordinate_type=coordinate_type, sign=sign, offset=offset)

    def __str__(self) -> str:
        if self.coordinate_type.is_missing():
            return ""
        return f"{self.coordinate_type}{self.sign}{self.offset}"


class CoordinateType(Enum):
    """Type of coordinate axis/meaning."""

    X = "X"
    Y = "Y"
    I = "I"  # noqa: E741
    J = "J"
    NULL = ""
    MISSING_X = "MISSING_X"
    MISSING_Y = "MISSING_Y"
    MISSING_I = "MISSING_I"
    MISSING_J = "MISSING_J"

    def to_missing(self) -> CoordinateType:
        """Map <coordinate> to MISSING_<coordinate>."""
        return _coordinate_type_to_missing_map[self]

    def is_missing(self) -> bool:
        """Check if coordinate is one of variants of missing coordinates."""
        return self in (
            CoordinateType.MISSING_X,
            CoordinateType.MISSING_Y,
            CoordinateType.MISSING_I,
            CoordinateType.MISSING_J,
        )

    def __str__(self) -> str:
        return self.value


_coordinate_type_to_missing_map = {
    CoordinateType.X: CoordinateType.MISSING_X,
    CoordinateType.Y: CoordinateType.MISSING_Y,
    CoordinateType.I: CoordinateType.MISSING_I,
    CoordinateType.J: CoordinateType.MISSING_J,
}


class CoordinateSign(Enum):
    """Coordinate sign."""

    Positive = "+"
    Negative = "-"

    def __str__(self) -> str:
        return "-" if self == CoordinateSign.Negative else ""
