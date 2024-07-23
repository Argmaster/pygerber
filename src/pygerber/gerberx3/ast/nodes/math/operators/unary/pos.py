"""`pygerber.nodes.math.operators.unary.Pos` module contains definition of `Pos`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class Pos(Expression):
    """Represents math expression pos."""

    operand: Expression

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_pos(self)
