"""`pygerber.nodes.g_codes.G01` module contains definition of `G01` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class G01(Node):
    """Represents G01 Gerber command."""

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_g01(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_g01
