"""`pygerber.nodes.math.operators.binary.Mul` module contains definition of `Mul`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

from pydantic import Field

from pygerber.gerber.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Mul(Expression):
    """Represents math expression multiplication operator."""

    head: Expression
    tail: List[Expression] = Field(min_length=1)

    def visit(self, visitor: AstVisitor) -> Mul:
        """Handle visitor call."""
        return visitor.on_mul(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Mul]:
        """Get callback function for the node."""
        return visitor.on_mul
