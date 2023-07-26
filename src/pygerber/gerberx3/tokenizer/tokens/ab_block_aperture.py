"""Wrapper for aperture select token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class BlockApertureBegin(Token):
    """Wrapper for AB begin token.

    Opens a block aperture statement and assigns its aperture number.
    """

    identifier: str

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        identifier: str = tokens["aperture_identifier"]
        return cls(identifier=identifier)

    def __str__(self) -> str:
        return f"AB{self.identifier}*"


class BlockApertureEnd(Token):
    """Wrapper for AB end token.

    Ends block aperture statement.
    """

    @classmethod
    def from_tokens(cls, **_tokens: Any) -> Self:
        """Initialize token object."""
        return cls()

    def __str__(self) -> str:
        return "AB*"
