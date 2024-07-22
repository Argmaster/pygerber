"""`pygerber.nodes.properties.SF` module contains definition of `SF` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class SF(Node):
    """Represents SF Gerber extended command."""

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_sf(self)
