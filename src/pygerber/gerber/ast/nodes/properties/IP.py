"""`pygerber.nodes.properties.IP` module contains definition of `IP` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.enums import ImagePolarity

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class IP(Node):
    """Represents IP Gerber extended command."""

    polarity: ImagePolarity

    def visit(self, visitor: AstVisitor) -> IP:
        """Handle visitor call."""
        return visitor.on_ip(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], IP]:
        """Get callback function for the node."""
        return visitor.on_ip
