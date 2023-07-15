"""Coordinate format token."""


from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class CoordinateFormat(Token):
    """Description of coordinate format token."""

    zeros_mode: TrailingZerosMode
    coordinate_mode: CoordinateMode
    x_format: AxisFormat
    y_format: AxisFormat

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        zeros_mode = TrailingZerosMode(tokens["zeros_mode"])
        coordinate_mode = CoordinateMode(tokens["coordinate_mode"])
        x_format = AxisFormat(
            integer=int(tokens["x_format"][0]),
            decimal=int(tokens["x_format"][1]),
        )
        y_format = AxisFormat(
            integer=int(tokens["y_format"][0]),
            decimal=int(tokens["y_format"][1]),
        )
        return cls(
            zeros_mode=zeros_mode,
            coordinate_mode=coordinate_mode,
            x_format=x_format,
            y_format=y_format,
        )


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
