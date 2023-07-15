"""Wrapper for plot operation token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class Draw(Token):
    """Wrapper for plot operation token.

    Outside a region statement D01 creates a draw or arc object with the current
    aperture. Inside it adds a draw/arc segment to the contour under construction. The
    current point is moved to draw/arc end point after the creation of the draw/arc.
    """

    x: Coordinate
    y: Coordinate
    i: Coordinate
    j: Coordinate

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
        i = tokens.get("i")
        i = (
            Coordinate(coordinate_type=CoordinateType.I, raw_offset=i)
            if i is not None
            else Coordinate(coordinate_type=CoordinateType.NULL, raw_offset="")
        )
        j = tokens.get("j")
        j = (
            Coordinate(coordinate_type=CoordinateType.J, raw_offset=j)
            if j is not None
            else Coordinate(coordinate_type=CoordinateType.NULL, raw_offset="")
        )
        return cls(x=x, y=y, i=i, j=j)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"{self.x}{self.y}{self.i}{self.j}D01*"
