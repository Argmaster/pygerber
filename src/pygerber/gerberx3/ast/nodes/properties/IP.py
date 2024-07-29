"""`pygerber.nodes.properties.IP` module contains definition of `IP` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class IP(Node):
    """Represents IP Gerber extended command."""

    polarity: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_ip(self)
