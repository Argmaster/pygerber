"""Wrapper for move operation token."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType
from pygerber.gerberx3.tokenizer.tokens.token import Token


class Move(Token):
    """Wrapper for move operation token.

    D02 moves the current point to the coordinate in the command. No graphical object is
    generated.
    """

    def __init__(
        self,
        x: str | None = None,
        y: str | None = None,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.x = (
            Coordinate(CoordinateType.X, x)
            if x is not None
            else Coordinate(CoordinateType.NULL, "")
        )
        self.y = (
            Coordinate(CoordinateType.Y, y)
            if y is not None
            else Coordinate(CoordinateType.NULL, "")
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"{self.x}{self.y}D02*"
