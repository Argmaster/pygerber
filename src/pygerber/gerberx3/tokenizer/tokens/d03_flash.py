"""Wrapper for flash operation token."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType
from pygerber.gerberx3.tokenizer.tokens.token import Token


class D03Flash(Token):
    """Wrapper for flash operation token.

    Creates a flash object with the current aperture. The current point is moved to the
    flash point.
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
        return f"{self.x}{self.y}D03*"
