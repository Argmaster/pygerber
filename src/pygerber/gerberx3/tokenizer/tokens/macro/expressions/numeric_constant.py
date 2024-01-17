"""Arithmetic expression token."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.tokenizer.tokens.macro.expressions.macro_expression import (
    MacroExpressionToken,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context
    from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2
    from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext


class NumericConstant(MacroExpressionToken):
    """Wrapper around numeric constant expression token."""

    def __init__(
        self,
        string: str,
        location: int,
        value: Decimal,
    ) -> None:
        super().__init__(string, location)
        self.value = value

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        value = Decimal(str(tokens["numeric_constant_value"]))

        return cls(
            string=string,
            location=location,
            value=value,
        )

    def to_parser2_expression(self, context: Parser2Context) -> Expression2:
        """Convert to `Expression2` descendant class."""
        return context.macro_expressions.constant(
            value=self.value,
        )

    def evaluate_numeric(self, _macro_context: MacroContext, state: State) -> Offset:
        """Evaluate numeric value of this macro expression."""
        return Offset.new(value=self.value, unit=state.get_units())

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code from iterable of tokens."""
        return f"{self.value}"

    def __str__(self) -> str:
        return f"{super().__str__()}::[{self.value}]"
