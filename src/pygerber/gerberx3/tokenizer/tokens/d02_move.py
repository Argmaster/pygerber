"""Wrapper for move operation token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class Move(Token):
    """Wrapper for move operation token.

    D02 moves the current point to the coordinate in the command. No graphical object is
    generated.
    """

    x: Coordinate
    y: Coordinate

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        x = tokens.get("x", "0")
        x = Coordinate.new(coordinate_type=CoordinateType.X, offset=x)
        y = tokens.get("y", "0")
        y = Coordinate.new(coordinate_type=CoordinateType.Y, offset=y)
        return cls(x=x, y=y)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"{self.x}{self.y}D02*"
