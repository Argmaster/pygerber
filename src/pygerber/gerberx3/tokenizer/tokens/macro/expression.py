"""In-macro expression token."""

from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.token import Token


class Expression(Token):
    """Wrapper for in-macro expression."""
