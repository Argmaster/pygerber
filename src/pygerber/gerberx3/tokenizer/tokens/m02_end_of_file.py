"""Wrapper for end of file token."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.token import Token


class M02EndOfFile(Token):
    """Wrapper for end of file token."""

    def __init__(self) -> None:
        """Initialize token object."""
        super().__init__()

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return "M02*"
