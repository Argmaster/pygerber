"""Comment token."""


from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self


class Comment(Expression):
    """Comment token.

    See section 4.1 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    content: str

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        content: str = tokens["string"]
        return cls(content=content)

    def __str__(self) -> str:
        return f"G04 {self.content}*"
