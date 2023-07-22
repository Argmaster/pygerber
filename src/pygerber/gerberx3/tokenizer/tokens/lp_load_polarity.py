"""Wrapper for load polarity token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.state_enums import Polarity
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class LoadPolarity(Token):
    """Wrapper for load polarity token.

    Loads the scale object transformation parameter.
    """

    polarity: Polarity

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        polarity = Polarity(tokens["polarity"])
        return cls(polarity=polarity)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"LP{self.polarity.value}*"
