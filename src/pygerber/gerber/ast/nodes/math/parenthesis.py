"""`pygerber.nodes.math.parenthesis` module contains definition of `Parenthesis`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Parenthesis(Expression):
    """Represents math expression expression."""

    inner: Expression

    def visit(self, visitor: AstVisitor) -> Parenthesis:
        """Handle visitor call."""
        return visitor.on_parenthesis(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Parenthesis]:
        """Get callback function for the node."""
        return visitor.on_parenthesis
