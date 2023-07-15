"""Wrapper for G01 mode set token."""
from __future__ import annotations

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
