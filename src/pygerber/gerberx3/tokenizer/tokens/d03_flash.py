"""Wrapper for flash operation token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class Flash(Token):
    """Wrapper for flash operation token.

    Creates a flash object with the current aperture. The current point is moved to the
    flash point.
    """

    x: Coordinate
    y: Coordinate

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        x = tokens.get("x")
        x = (
            Coordinate(coordinate_type=CoordinateType.X, raw_offset=x)
            if x is not None
            else Coordinate(coordinate_type=CoordinateType.NULL, raw_offset="")
        )
        y = tokens.get("y")
        y = (
            Coordinate(coordinate_type=CoordinateType.Y, raw_offset=y)
            if y is not None
            else Coordinate(coordinate_type=CoordinateType.NULL, raw_offset="")
        )
        return cls(x=x, y=y)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"{self.x}{self.y}D03*"
