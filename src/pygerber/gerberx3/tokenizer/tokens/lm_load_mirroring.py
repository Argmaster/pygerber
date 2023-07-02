"""Wrapper for load mirroring token."""
from __future__ import annotations

from enum import Enum

from pygerber.gerberx3.tokenizer.tokens.token import Token


class LoadMirroring(Token):
    """Wrapper for load mirroring token.

    Loads the mirror object transformation parameter.
    """

    def __init__(self, mirroring: str) -> None:
        """Initialize token object."""
        super().__init__()
        self.mirroring = Mirroring(mirroring)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"LM{self.mirroring.value}*"


class Mirroring(Enum):
    """Aperture mirroring."""

    NoMirroring = "N"
    XY = "XY"
    X = "X"
    Y = "Y"
