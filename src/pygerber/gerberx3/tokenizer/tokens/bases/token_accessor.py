"""Accessor for token objects in AST."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Sequence

if TYPE_CHECKING:
    from pygerber.gerberx3.tokenizer.tokens.bases.token import Token


class TokenAccessor:
    """Accessor containing reference to token and its parent group."""

    def __init__(
        self,
        token: Optional[Token],
        parent: Optional[TokenAccessor] = None,
        tokens: Sequence[Token] = (),
        token_index: int = 0,
    ) -> None:
        self.token = token
        self.parent = parent
        self.tokens = tokens
        self.token_index = token_index
