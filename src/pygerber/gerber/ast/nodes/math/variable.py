"""`pygerber.nodes.math.variable` module contains definition of `Variable` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Variable(Expression):
    """Represents math expression variable."""

    variable: str

    def visit(self, visitor: AstVisitor) -> Variable:
        """Handle visitor call."""
        return visitor.on_variable(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Variable]:
        """Get callback function for the node."""
        return visitor.on_variable
