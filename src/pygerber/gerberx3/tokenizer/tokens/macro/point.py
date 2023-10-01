"""Point wrapper token."""


from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.gerberx3.tokenizer.tokens.macro.numeric_expression import (
    NumericExpression,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self


class Point(Expression):
    """Point wrapper token."""

    def __init__(
        self,
        string: str,
        location: int,
        x: NumericExpression,
        y: NumericExpression,
    ) -> None:
        super().__init__(string, location)
        self.x = x
        self.y = y

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        x = NumericExpression.ensure_type(tokens["x"])
        y = NumericExpression.ensure_type(tokens["y"])

        return cls(
            string=string,
            location=location,
            x=x,
            y=y,
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code from iterable of tokens."""
        return (
            f"{self.x.get_gerber_code(indent, endline)},"
            f"{self.y.get_gerber_code(indent, endline)}"
        )

    def __str__(self) -> str:
        return f"{super().__str__()}::[{self.x}, {self.y}]"
