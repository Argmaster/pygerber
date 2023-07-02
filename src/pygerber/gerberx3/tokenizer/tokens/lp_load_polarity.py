"""Wrapper for load polarity token."""
from __future__ import annotations

from enum import Enum

from pygerber.gerberx3.tokenizer.tokens.token import Token


class LoadPolarity(Token):
    """Wrapper for load polarity token.

    Loads the scale object transformation parameter.
    """

    def __init__(self, polarity: str) -> None:
        """Initialize token object."""
        super().__init__()
        self.polarity = Polarity(polarity)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"LP{self.polarity.value}*"


class Polarity(Enum):
    """Aperture polarity."""

    Clear = "C"
    Dark = "D"
