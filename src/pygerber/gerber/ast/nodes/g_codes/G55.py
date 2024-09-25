"""`pygerber.nodes.g_codes.G55` module contains definition of `G55` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.g_codes.G import G

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class G55(G):
    """Represents G55 Gerber command."""

    def visit(self, visitor: AstVisitor) -> G55:
        """Handle visitor call."""
        return visitor.on_g55(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], G55]:
        """Get callback function for the node."""
        return visitor.on_g55
