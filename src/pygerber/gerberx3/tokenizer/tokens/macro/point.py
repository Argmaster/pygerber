"""Point wrapper token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.parser2.macro2.point2 import Point2
from pygerber.gerberx3.tokenizer.tokens.bases.token import Token
from pygerber.gerberx3.tokenizer.tokens.macro.expressions.macro_expression import (
    MacroExpressionToken,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Point(Token):
    """Point wrapper token."""

    def __init__(
        self,
        string: str,
        location: int,
        x: MacroExpressionToken,
        y: MacroExpressionToken,
    ) -> None:
        super().__init__(string, location)
        self.x = x
        self.y = y

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        x = MacroExpressionToken.ensure_type(tokens["x"])
        y = MacroExpressionToken.ensure_type(tokens["y"])

        return cls(
            string=string,
            location=location,
            x=x,
            y=y,
        )

    def to_parser2_point2(self, context: Parser2Context) -> Point2:
        """Convert to `Expression2` descendant class."""
        return Point2(
            x=self.x.to_parser2_expression(context=context),
            y=self.y.to_parser2_expression(context=context),
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
