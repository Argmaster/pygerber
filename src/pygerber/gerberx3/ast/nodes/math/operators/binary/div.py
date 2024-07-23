"""`pygerber.nodes.math.operators.binary.Div` module contains definition of `Div`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from pydantic import Field

from pygerber.gerberx3.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class Div(Expression):
    """Represents math expression division operator."""

    operands: List[Expression] = Field(min_length=2)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_div(self)
