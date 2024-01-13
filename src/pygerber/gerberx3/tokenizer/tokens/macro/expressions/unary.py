"""Arithmetic expression token."""

from __future__ import annotations

from operator import neg, pos
from typing import TYPE_CHECKING, Any, Callable

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.tokenizer.tokens.macro.expressions.errors import (
    InvalidArithmeticExpressionError,
)
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


class UnaryOperator(MacroExpressionToken):
    """Operator with one operand."""

    def __init__(
        self,
        string: str,
        location: int,
        operand: MacroExpressionToken,
    ) -> None:
        super().__init__(string, location)
        self.operand = operand
        self.operator: Callable[[Any], Any] = neg
        self.sign = "-"

    @classmethod
    def new(
        cls,
        string: str,
        location: int,
        tokens: ParseResults,
    ) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        operand, *_ = tokens.as_list()[0]

        if not isinstance(operand, MacroExpressionToken):
            raise TypeError(operand)

        return cls(string, location, operand)

    def to_parser2_expression(self, context: Parser2Context) -> Expression2:
        """Convert to `Expression2` descendant class."""
        raise NotImplementedError

    def evaluate_numeric(self, macro_context: MacroContext, state: State) -> Offset:
        """Evaluate numeric value of this macro expression."""
        operand = self.operand.evaluate_numeric(macro_context, state)
        output = self.operator(operand)

        if not isinstance(output, Offset):
            raise InvalidArithmeticExpressionError

        return output

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code from iterable of tokens."""
        return (
            f"{self.sign}{self.operand.get_gerber_code(indent=indent, endline=endline)}"
        )

    def __str__(self) -> str:
        return f"{super().__str__()}::[{self.operand}]"


class NegationOperator(UnaryOperator):
    """Negation operation."""

    def __init__(
        self,
        string: str,
        location: int,
        operand: MacroExpressionToken,
    ) -> None:
        super().__init__(string, location, operand)
        self.operator = neg
        self.sign = "-"

    def to_parser2_expression(self, context: Parser2Context) -> Expression2:
        """Convert to `UnaryMinusExpression2`."""
        return context.macro_expressions.negation(
            op=self.operand.to_parser2_expression(context),
        )


class PositiveOperator(UnaryOperator):
    """Negation operation."""

    def __init__(
        self,
        string: str,
        location: int,
        operand: MacroExpressionToken,
    ) -> None:
        super().__init__(string, location, operand)
        self.operator = pos
        self.sign = "+"

    def to_parser2_expression(self, context: Parser2Context) -> Expression2:
        """Convert to `UnaryPlusExpression2`."""
        return context.macro_expressions.positive(
            op=self.operand.to_parser2_expression(context),
        )
