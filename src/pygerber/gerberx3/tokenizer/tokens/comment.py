"""Comment token."""


from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.token import Token


class Comment(Token):
    """Comment token."""

    def __init__(self, string: str) -> None:
        """Initialize token object."""
        super().__init__()
        self.content = string

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"G04 {self.content}*"
