"""Comment token."""


from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self


class Comment(Expression):
    """Comment token."""

    content: str

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        content: str = tokens["string"]
        return cls(content=content)

    def __str__(self) -> str:
        return f"G04 {self.content}*"
