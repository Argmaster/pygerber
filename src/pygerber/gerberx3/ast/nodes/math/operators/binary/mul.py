"""`pygerber.nodes.math.operators.binary.Mul` module contains definition of `Mul`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

from pydantic import Field

from pygerber.gerberx3.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class Mul(Expression):
    """Represents math expression multiplication operator."""

    head: Expression
    tail: List[Expression] = Field(min_length=1)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_mul(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_mul
