"""Common base class for all macro specific tokens."""

from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.token import Token


class Element(Token):
    """Common base class for all macro specific tokens."""

    def __init__(self) -> None:
        """Initialize token object."""
        super().__init__()
