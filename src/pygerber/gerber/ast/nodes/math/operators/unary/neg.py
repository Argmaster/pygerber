"""`pygerber.nodes.math.operators.unary.Neg` module contains definition of `Neg`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Neg(Expression):
    """Represents math expression neg."""

    operand: Expression

    def visit(self, visitor: AstVisitor) -> Neg:
        """Handle visitor call."""
        return visitor.on_neg(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Neg]:
        """Get callback function for the node."""
        return visitor.on_neg
