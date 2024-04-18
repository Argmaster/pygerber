"""`binary2` module contain classes wrapping binary operations within macro."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2

if TYPE_CHECKING:
    from decimal import Decimal

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class BinaryOperator2(Expression2):
    """Single binary operation."""

    lhs: Expression2
    rhs: Expression2


class Addition2(BinaryOperator2):
    """Addition expression."""

    def on_parser2_eval_expression(self, context: Parser2Context) -> Decimal:
        """Reduce expression to numerical value."""
        return self.lhs.on_parser2_eval_expression(
            context,
        ) + self.rhs.on_parser2_eval_expression(context)


class Subtraction2(BinaryOperator2):
    """Subtract expression."""

    def on_parser2_eval_expression(self, context: Parser2Context) -> Decimal:
        """Reduce expression to numerical value."""
        return self.lhs.on_parser2_eval_expression(
            context,
        ) - self.rhs.on_parser2_eval_expression(context)


class Multiplication2(BinaryOperator2):
    """Multiply expression."""

    def on_parser2_eval_expression(self, context: Parser2Context) -> Decimal:
        """Reduce expression to numerical value."""
        return self.lhs.on_parser2_eval_expression(
            context,
        ) * self.rhs.on_parser2_eval_expression(context)


class Division2(BinaryOperator2):
    """Divide expression."""

    def on_parser2_eval_expression(self, context: Parser2Context) -> Decimal:
        """Reduce expression to numerical value."""
        return self.lhs.on_parser2_eval_expression(
            context,
        ) / self.rhs.on_parser2_eval_expression(context)
