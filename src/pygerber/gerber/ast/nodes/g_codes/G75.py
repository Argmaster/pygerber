"""`pygerber.nodes.g_codes.G75` module contains definition of `G75` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.g_codes.G import G

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class G75(G):
    """Represents G75 Gerber command."""

    def visit(self, visitor: AstVisitor) -> G75:
        """Handle visitor call."""
        return visitor.on_g75(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], G75]:
        """Get callback function for the node."""
        return visitor.on_g75
