"""Arithmetic expression token."""

from __future__ import annotations

from operator import add, mul, sub, truediv
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


class BinaryOperator(MacroExpressionToken):
    """Operation with two operands."""

    def __init__(
        self,
        string: str,
        location: int,
        left: MacroExpressionToken,
        right: MacroExpressionToken,
    ) -> None:
        super().__init__(string, location)
        self.left = left
        self.right = right
        self.operator: Callable[[Any, Any], Any] = add
        self.sign = "+"

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
        left, right = tokens[0]
        return cls(
            string,
            location,
            MacroExpressionToken.ensure_type(left),
            MacroExpressionToken.ensure_type(right),
        )

    def to_parser2_expression(self, context: Parser2Context) -> Expression2:
        """Convert to `Expression2` descendant class."""
        raise NotImplementedError

    def evaluate_numeric(self, macro_context: MacroContext, state: State) -> Offset:
        """Evaluate numeric value of this macro expression."""
        left = self.left.evaluate_numeric(macro_context, state)
        right = self.right.evaluate_numeric(macro_context, state)
        output = self.operator(left, right)

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
            f"{self.left.get_gerber_code(indent=indent, endline=endline)}{self.sign}"
            f"{self.right.get_gerber_code(indent=indent, endline=endline)}"
        )

    def __str__(self) -> str:
        return f"{super().__str__()}::[{self.left}, {self.right}]"


class MultiplicationOperator(BinaryOperator):
    """Operation with two operands."""

    def __init__(
        self,
        string: str,
        location: int,
        left: MacroExpressionToken,
        right: MacroExpressionToken,
    ) -> None:
        super().__init__(string, location, left, right)
        self.operator: Callable[[Any, Any], Any] = mul
        self.sign = "x"

    def to_parser2_expression(self, context: Parser2Context) -> Expression2:
        """Convert to `Expression2` descendant class."""
        return context.macro_expressions.multiplication(
            lhs=self.left.to_parser2_expression(context),
            rhs=self.right.to_parser2_expression(context),
        )


class DivisionOperator(BinaryOperator):
    """Operation with two operands."""

    def __init__(
        self,
        string: str,
        location: int,
        left: MacroExpressionToken,
        right: MacroExpressionToken,
    ) -> None:
        super().__init__(string, location, left, right)
        self.operator: Callable[[Any, Any], Any] = truediv
        self.sign = "/"

    def to_parser2_expression(self, context: Parser2Context) -> Expression2:
        """Convert to `Expression2` descendant class."""
        return context.macro_expressions.division(
            lhs=self.left.to_parser2_expression(context),
            rhs=self.right.to_parser2_expression(context),
        )


class AdditionOperator(BinaryOperator):
    """Operation with two operands."""

    def __init__(
        self,
        string: str,
        location: int,
        left: MacroExpressionToken,
        right: MacroExpressionToken,
    ) -> None:
        super().__init__(string, location, left, right)
        self.operator: Callable[[Any, Any], Any] = add
        self.sign = "+"

    def to_parser2_expression(self, context: Parser2Context) -> Expression2:
        """Convert to `Expression2` descendant class."""
        return context.macro_expressions.addition(
            lhs=self.left.to_parser2_expression(context),
            rhs=self.right.to_parser2_expression(context),
        )


class SubtractionOperator(BinaryOperator):
    """Operation with two operands."""

    def __init__(
        self,
        string: str,
        location: int,
        left: MacroExpressionToken,
        right: MacroExpressionToken,
    ) -> None:
        super().__init__(string, location, left, right)
        self.operator: Callable[[Any, Any], Any] = sub
        self.sign = "-"

    def to_parser2_expression(self, context: Parser2Context) -> Expression2:
        """Convert to `Expression2` descendant class."""
        return context.macro_expressions.subtraction(
            lhs=self.left.to_parser2_expression(context),
            rhs=self.right.to_parser2_expression(context),
        )
