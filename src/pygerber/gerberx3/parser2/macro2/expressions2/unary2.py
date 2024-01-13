"""`unary2` module contain classes wrapping unary operations within macro."""
from __future__ import annotations

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2


class UnaryOperator2(Expression2):
    """Single binary operation."""

    op: Expression2


class Negation2(UnaryOperator2):
    """Unary minus operation."""


class Positive2(UnaryOperator2):
    """Unary plus operation."""
