"""`pygerber.nodes.math.operators.binary.Sub` module contains definition of `Sub`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class Sub(Node):
    """Represents math expression subtraction operator."""

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_sub(self)
