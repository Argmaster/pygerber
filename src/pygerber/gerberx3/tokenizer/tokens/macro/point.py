"""Point wrapper token."""


from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.gerberx3.tokenizer.tokens.macro.numeric_expression import (
    NumericExpression,
)
from pygerber.sequence_tools import unwrap

if TYPE_CHECKING:
    from typing_extensions import Self


class Point(Expression):
    """Point wrapper token."""

    x: NumericExpression
    y: NumericExpression

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        x: NumericExpression = unwrap(tokens["x"])
        y: NumericExpression = unwrap(tokens["y"])

        return cls(x=x, y=y)

    def __str__(self) -> str:
        return f"{self.x},{self.y}"
