"""`binary2` module contain classes wrapping binary operations within macro."""
from __future__ import annotations

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2


class BinaryOperator2(Expression2):
    """Single binary operation."""

    lhs: Expression2
    rhs: Expression2


class Addition2(BinaryOperator2):
    """Addition expression."""


class Subtraction2(BinaryOperator2):
    """Subtract expression."""


class Multiplication2(BinaryOperator2):
    """Multiply expression."""


class Division2(BinaryOperator2):
    """Divide expression."""
