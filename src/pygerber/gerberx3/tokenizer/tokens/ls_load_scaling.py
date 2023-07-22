"""Wrapper for load scaling token."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class LoadScaling(Token):
    """Wrapper for load scaling token.

    Loads the scaling object transformation parameter.
    """

    scaling: Decimal

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        scaling = Decimal(tokens["scaling"])
        return cls(scaling=scaling)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"LS{self.scaling}*"
