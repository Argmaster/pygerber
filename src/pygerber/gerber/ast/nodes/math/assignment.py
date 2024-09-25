"""`pygerber.nodes.math.assignment` module contains definition of `Assignment` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.math.expression import Expression
from pygerber.gerber.ast.nodes.math.variable import Variable

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Assignment(Node):
    """Represents math expression variable."""

    variable: Variable
    expression: Expression

    def visit(self, visitor: AstVisitor) -> Assignment:
        """Handle visitor call."""
        return visitor.on_assignment(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Assignment]:
        """Get callback function for the node."""
        return visitor.on_assignment
