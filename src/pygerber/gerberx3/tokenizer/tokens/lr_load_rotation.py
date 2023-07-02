"""Wrapper for load rotation token."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.token import Token


class LoadRotation(Token):
    """Wrapper for load rotation token.

    Loads the rotation object transformation parameter.
    """

    def __init__(self, rotation: str) -> None:
        """Initialize token object."""
        super().__init__()
        self.rotation = float(rotation)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"LR{self.rotation}*"
