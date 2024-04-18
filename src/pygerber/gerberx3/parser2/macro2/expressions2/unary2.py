"""`unary2` module contain classes wrapping unary operations within macro."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2

if TYPE_CHECKING:
    from decimal import Decimal

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class UnaryOperator2(Expression2):
    """Single binary operation."""

    op: Expression2


class Negation2(UnaryOperator2):
    """Unary minus operation."""

    def on_parser2_eval_expression(self, context: Parser2Context) -> Decimal:
        """Reduce expression to numerical value."""
        return -self.op.on_parser2_eval_expression(context)


class Positive2(UnaryOperator2):
    """Unary plus operation."""

    def on_parser2_eval_expression(self, context: Parser2Context) -> Decimal:
        """Reduce expression to numerical value."""
        return self.op.on_parser2_eval_expression(context)
