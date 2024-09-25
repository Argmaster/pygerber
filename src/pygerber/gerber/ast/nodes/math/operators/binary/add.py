"""`pygerber.nodes.math.operators.binary.Add` module contains definition of `Add`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

from pydantic import Field

from pygerber.gerber.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Add(Expression):
    """Represents math expression addition operator."""

    head: Expression
    tail: List[Expression] = Field(min_length=1)

    def visit(self, visitor: AstVisitor) -> Add:
        """Handle visitor call."""
        return visitor.on_add(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Add]:
        """Get callback function for the node."""
        return visitor.on_add
