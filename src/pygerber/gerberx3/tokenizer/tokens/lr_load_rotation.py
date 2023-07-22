"""Wrapper for load rotation token."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class LoadRotation(Token):
    """Wrapper for load rotation token.

    Loads the rotation object transformation parameter.
    """

    rotation: Decimal

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        rotation = Decimal(tokens["rotation"])
        return cls(rotation=rotation)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"LR{self.rotation}*"
