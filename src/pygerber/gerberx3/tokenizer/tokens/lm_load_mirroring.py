"""Wrapper for load mirroring token."""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class LoadMirroring(Token):
    """Wrapper for load mirroring token.

    Loads the mirror object transformation parameter.
    """

    mirroring: Mirroring

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        mirroring = Mirroring(tokens["mirroring"])
        return cls(mirroring=mirroring)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"LM{self.mirroring.value}*"


class Mirroring(Enum):
    """Aperture mirroring."""

    NoMirroring = "N"
    XY = "XY"
    X = "X"
    Y = "Y"
