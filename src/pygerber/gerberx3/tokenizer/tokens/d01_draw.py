"""Wrapper for plot operation token."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType
from pygerber.gerberx3.tokenizer.tokens.token import Token


class D01Draw(Token):
    """Wrapper for plot operation token.

    Outside a region statement D01 creates a draw or arc object with the current
    aperture. Inside it adds a draw/arc segment to the contour under construction. The
    current point is moved to draw/arc end point after the creation of the draw/arc.
    """

    def __init__(
        self,
        x: str | None = None,
        y: str | None = None,
        i: str | None = None,
        j: str | None = None,
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
        self.i = (
            Coordinate(CoordinateType.I, i)
            if i is not None
            else Coordinate(CoordinateType.NULL, "")
        )
        self.j = (
            Coordinate(CoordinateType.J, j)
            if j is not None
            else Coordinate(CoordinateType.NULL, "")
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"{self.x}{self.y}{self.i}{self.j}D01*"
