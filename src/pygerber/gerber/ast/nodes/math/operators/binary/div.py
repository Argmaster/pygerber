"""`pygerber.nodes.math.operators.binary.Div` module contains definition of `Div`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

from pydantic import Field

from pygerber.gerber.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Div(Expression):
    """Represents math expression division operator."""

    head: Expression
    tail: List[Expression] = Field(min_length=1)

    def visit(self, visitor: AstVisitor) -> Div:
        """Handle visitor call."""
        return visitor.on_div(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Div]:
        """Get callback function for the node."""
        return visitor.on_div
