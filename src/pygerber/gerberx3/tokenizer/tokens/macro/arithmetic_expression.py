"""Arithmetic expression token."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, cast

from pygerber.gerberx3.tokenizer.errors import TokenizerError
from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.sequence_tools import unwrap

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

ARITHMETIC_EXPRESSION_TOKEN_COUNT = 3
ARITHMETIC_EXPRESSION_NOT_ENOUGH_TOKEN_COUNT = 2


class ArithmeticExpression(Expression):
    """Wrapper for arithmetic expression."""

    def __init__(
        self,
        left: Expression,
        operator: ArithmeticOperator,
        right: Expression,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.left = unwrap(left)
        self.operator = unwrap(operator)
        self.right = unwrap(right)

    @classmethod
    def new(cls, _string: str, _location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        return cls._build(tokens.as_list()[0])

    @classmethod
    def _build(cls, tokens: list[ParseResults]) -> Self:
        (left, operator, *rest) = tokens

        right: Expression

        if len(rest) >= ARITHMETIC_EXPRESSION_TOKEN_COUNT:
            right = cls._build(rest)

        elif len(rest) == ARITHMETIC_EXPRESSION_NOT_ENOUGH_TOKEN_COUNT:
            raise InvalidArithmeticExpressionError

        elif len(rest) == 1:
            (right,) = cast("tuple[Expression]", rest)

        else:
            raise AssertionError

        return cls(
            left=cast(Expression, left),
            operator=ArithmeticOperator(operator),
            right=right,
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"{self.left}{self.operator.value}{self.right}"


class InvalidArithmeticExpressionError(TokenizerError):
    """Raised when it's not possible to construct valid arithmetic expression."""


class ArithmeticOperator(Enum):
    """Enum of possible math operations."""

    MULTIPLICATION = "x"
    DIVISION = "/"
    ADDITION = "+"
    SUBTRACTION = "-"


class NumericConstant(Expression):
    """Wrapper around numeric constant expression token."""

    def __init__(self, value: str) -> None:
        """Initialize token object."""
        super().__init__()
        self.value = float(value)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return str(self.value)
