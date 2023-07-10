"""Comment token."""


from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.g04_comment import Comment


class MacroComment(Comment):
    """Macro comment token."""

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"0 {self.content}*"
