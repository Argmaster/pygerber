"""`pygerber.nodes.math.operators.unary.Neg` module contains definition of `Neg`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class Neg(Expression):
    """Represents math expression neg."""

    operand: Expression

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_neg(self)
