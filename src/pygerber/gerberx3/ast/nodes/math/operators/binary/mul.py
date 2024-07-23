"""`pygerber.nodes.math.operators.binary.Mul` module contains definition of `Mul`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from pydantic import Field

from pygerber.gerberx3.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class Mul(Expression):
    """Represents math expression multiplication operator."""

    operands: List[Expression] = Field(min_length=2)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_mul(self)
