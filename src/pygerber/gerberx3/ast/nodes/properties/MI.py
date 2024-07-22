"""`pygerber.nodes.properties.MI` module contains definition of `MI` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class MI(Node):
    """Represents MI Gerber extended command."""

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_mi(self)
