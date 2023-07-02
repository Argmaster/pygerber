"""Wrapper for G03 mode set token."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.token import Token


class G03SetCounterclockwiseCircular(Token):
    """Wrapper for G03 mode set token.

    Sets linear/circular mode to counterclockwise circular.
    """

    def __init__(self) -> None:
        """Initialize token object."""
        super().__init__()

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return "G03*"
