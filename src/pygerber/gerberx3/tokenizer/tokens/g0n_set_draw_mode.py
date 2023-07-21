"""Wrapper for G01 mode set token."""
from __future__ import annotations

from enum import Enum

from pygerber.gerberx3.tokenizer.tokens.token import Token


class SetLinear(Token):
    """Wrapper for G01 mode set token.

    Sets linear/circular mode to linear.
    """

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return "G01*"


class SetClockwiseCircular(Token):
    """Wrapper for G02 mode set token.

    Sets linear/circular mode to clockwise circular.
    """

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return "G02*"


class SetCounterclockwiseCircular(Token):
    """Wrapper for G03 mode set token.

    Sets linear/circular mode to counterclockwise circular.
    """

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return "G03*"


class DrawMode(Enum):
    """Drawing mode."""

    Linear = "G01"
    """In linear plot mode a D01 operation generates a linear segment, from the current
    point to the (X, Y) coordinates in the command. The current point is then set to the
    (X, Y) coordinates.Outside a region statement the segment is stroked with the
    current aperture to create a draw graphical object. In a region statement the
    segment is added to the contour under construction."""

    ClockwiseCircular = "G02"
    """In circular plot mode a D01 operation generates an arc segment, from the current
    point to the (X, Y) coordinates in the command. The current point is then set to the
    (X, Y) coordinates. Outside a region statement the segment is stroked with the
    current aperture to create an arc graphical object. In a region statement the
    segment is added to the contour under construction. For compatibility with older
    versions of the Gerber format, a G75* must be issued before the first D01 in
    circular mode."""

    CounterclockwiseCircular = "G03"
    """In circular plot mode a D01 operation generates an arc segment, from the current
    point to the (X, Y) coordinates in the command. The current point is then set to the
    (X, Y) coordinates. Outside a region statement the segment is stroked with the
    current aperture to create an arc graphical object. In a region statement the
    segment is added to the contour under construction. For compatibility with older
    versions of the Gerber format, a G75* must be issued before the first D01 in
    circular mode."""
