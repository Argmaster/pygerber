"""Coordinate format token."""


from __future__ import annotations

from enum import Enum

from pydantic import BaseModel
from pygerber.gerberx3.tokenizer.tokens.token import Token


class CoordinateFormat(Token):
    """Description of coordinate format token."""

    def __init__(
        self,
        zeros_mode: str,
        coordinate_mode: str,
        x_format: str,
        y_format: str,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.zeros_mode = TrailingZerosMode(zeros_mode)
        self.coordinate_mode = CoordinateMode(coordinate_mode)
        self.x_format = AxisFormat(integer=int(x_format[0]), decimal=int(x_format[1]))
        self.y_format = AxisFormat(integer=int(y_format[0]), decimal=int(y_format[1]))

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"%FS{self.zeros_mode.value}{self.coordinate_mode.value}\
                X{self.x_format.integer}{self.x_format.decimal}\
                Y{self.y_format.integer}{self.y_format.decimal}"


class TrailingZerosMode(Enum):
    """Coordinate format mode.

    GerberX3 supports only one, L, the other is required for backwards compatibility.
    """

    KeepZeros = "L"
    OmitZeros = "T"


class CoordinateMode(Enum):
    """Coordinate format mode.

    GerberX3 supports only one, A, the other required for backwards compatibility.
    """

    Absolute = "A"
    Incremental = "I"


class AxisFormat(BaseModel):
    """Wrapper for single axis format."""

    integer: int
    decimal: int
