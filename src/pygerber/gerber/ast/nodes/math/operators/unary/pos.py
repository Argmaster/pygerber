"""`pygerber.nodes.math.operators.unary.Pos` module contains definition of `Pos`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Pos(Expression):
    """Represents math expression pos."""

    operand: Expression

    def visit(self, visitor: AstVisitor) -> Pos:
        """Handle visitor call."""
        return visitor.on_pos(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Pos]:
        """Get callback function for the node."""
        return visitor.on_pos
