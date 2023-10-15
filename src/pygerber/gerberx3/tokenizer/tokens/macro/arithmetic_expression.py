"""Arithmetic expression token."""

from __future__ import annotations

from operator import add, mul, neg, pos, sub, truediv
from typing import TYPE_CHECKING, Any, Callable

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.tokenizer.errors import TokenizerError
from pygerber.gerberx3.tokenizer.tokens.macro.numeric_expression import (
    NumericExpression,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext


class UnaryOperator(NumericExpression):
    """Operator with one operand."""

    def __init__(self, string: str, location: int, operand: NumericExpression) -> None:
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

        if not isinstance(operand, NumericExpression):
            raise TypeError(operand)

        return cls(string, location, operand)

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

    def __init__(self, string: str, location: int, operand: NumericExpression) -> None:
        super().__init__(string, location, operand)
        self.operator = neg
        self.sign = "-"


class PositiveOperator(UnaryOperator):
    """Negation operation."""

    def __init__(self, string: str, location: int, operand: NumericExpression) -> None:
        super().__init__(string, location, operand)
        self.operator = pos
        self.sign = "+"


class BinaryOperator(NumericExpression):
    """Operation with two operands."""

    def __init__(
        self,
        string: str,
        location: int,
        left: NumericExpression,
        right: NumericExpression,
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
            NumericExpression.ensure_type(left),
            NumericExpression.ensure_type(right),
        )

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
        left: NumericExpression,
        right: NumericExpression,
    ) -> None:
        super().__init__(string, location, left, right)
        self.operator: Callable[[Any, Any], Any] = mul
        self.sign = "x"


class DivisionOperator(BinaryOperator):
    """Operation with two operands."""

    def __init__(
        self,
        string: str,
        location: int,
        left: NumericExpression,
        right: NumericExpression,
    ) -> None:
        super().__init__(string, location, left, right)
        self.operator: Callable[[Any, Any], Any] = truediv
        self.sign = "/"


class AdditionOperator(BinaryOperator):
    """Operation with two operands."""

    def __init__(
        self,
        string: str,
        location: int,
        left: NumericExpression,
        right: NumericExpression,
    ) -> None:
        super().__init__(string, location, left, right)
        self.operator: Callable[[Any, Any], Any] = add
        self.sign = "+"


class SubtractionOperator(BinaryOperator):
    """Operation with two operands."""

    def __init__(
        self,
        string: str,
        location: int,
        left: NumericExpression,
        right: NumericExpression,
    ) -> None:
        super().__init__(string, location, left, right)
        self.operator: Callable[[Any, Any], Any] = sub
        self.sign = "-"


class InvalidArithmeticExpressionError(TokenizerError):
    """Raised when it's not possible to construct valid arithmetic expression."""
