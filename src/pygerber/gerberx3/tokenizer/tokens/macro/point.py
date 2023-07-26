"""Point wrapper token."""


from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import Self
from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.sequence_tools import unwrap


class Point(Expression):
    """Point wrapper token."""

    x: Expression
    y: Expression

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        x: Expression = unwrap(tokens["x"])
        y: Expression = unwrap(tokens["y"])

        return cls(x=x, y=y)

    def __str__(self) -> str:
        return f"{self.x},{self.y}"
