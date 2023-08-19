"""Arithmetic expression token."""

from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Any, cast

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

ARITHMETIC_EXPRESSION_TOKEN_COUNT = 3
ARITHMETIC_EXPRESSION_SINGLE_OPERAND_TOKEN_COUNT = 2


class ArithmeticExpression(NumericExpression):
    """Wrapper for arithmetic expression."""

    left: NumericExpression
    operator: ArithmeticOperator
    right: NumericExpression

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        left = tokens["left"]
        operator = str(tokens["operator"]).lower()
        right = tokens["right"]

        return cls(left=left, operator=ArithmeticOperator(operator), right=right)

    @classmethod
    def new(cls, _string: str, _location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        return cls._build(tokens.as_list()[0])

    @classmethod
    def _build(cls, tokens: list[ParseResults]) -> Self:
        left: Any
        operator: Any

        (left, operator, *rest) = tokens

        right: NumericExpression

        if len(rest) >= ARITHMETIC_EXPRESSION_TOKEN_COUNT:
            right = cls._build(rest)

        elif len(rest) == ARITHMETIC_EXPRESSION_SINGLE_OPERAND_TOKEN_COUNT:
            raise InvalidArithmeticExpressionError

        elif len(rest) == 1:
            (right,) = cast("tuple[NumericExpression]", rest)

        elif len(rest) == 0:
            (left, operator, right) = (
                NumericConstant(value=Decimal("0.0")),
                left,
                operator,
            )

        else:
            raise AssertionError

        return cls.from_tokens(
            left=left,
            operator=operator,
            right=right,
        )

    def evaluate_numeric(self, macro_context: MacroContext, state: State) -> Offset:
        """Evaluate numeric value of this macro expression."""
        left = self.left.evaluate_numeric(macro_context, state)
        right = self.right.evaluate_numeric(macro_context, state)
        output = self.operator.evaluate(left, right)

        if not isinstance(output, Offset):
            raise InvalidArithmeticExpressionError

        return output

    def __str__(self) -> str:
        return f"{self.left}{self.operator.value}{self.right}"


class InvalidArithmeticExpressionError(TokenizerError):
    """Raised when it's not possible to construct valid arithmetic expression."""


class ArithmeticOperator(Enum):
    """Enum of possible math operations."""

    MULTIPLICATION = "x"
    DIVISION = "/"
    ADDITION = "+"
    SUBTRACTION = "-"

    def evaluate(self, left: Any, right: Any) -> Any:
        """Evaluate corresponding arithmetic operator on given operands."""
        if self == ArithmeticOperator.MULTIPLICATION:
            return left * right

        if self == ArithmeticOperator.DIVISION:
            return left / right

        if self == ArithmeticOperator.ADDITION:
            return left + right

        if self == ArithmeticOperator.SUBTRACTION:
            return left - right

        raise AssertionError


class NumericConstant(NumericExpression):
    """Wrapper around numeric constant expression token."""

    value: Decimal

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        value = Decimal(tokens["numeric_constant_value"])

        return cls(value=value)

    def evaluate_numeric(self, _macro_context: MacroContext, state: State) -> Offset:
        """Evaluate numeric value of this macro expression."""
        return Offset.new(value=self.value, unit=state.get_units())

    def __str__(self) -> str:
        return str(self.value)
