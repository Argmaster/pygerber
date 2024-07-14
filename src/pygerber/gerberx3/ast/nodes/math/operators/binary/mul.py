"""`pygerber.nodes.math.operators.binary.Mul` module contains definition of `Mul`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class Mul(Node):
    """Represents math expression multiplication operator."""

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_mul(self)
