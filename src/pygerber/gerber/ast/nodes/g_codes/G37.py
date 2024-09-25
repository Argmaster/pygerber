"""`pygerber.nodes.g_codes.G37` module contains definition of `G37` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.g_codes.G import G

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class G37(G):
    """Represents G37 Gerber command."""

    def visit(self, visitor: AstVisitor) -> G37:
        """Handle visitor call."""
        return visitor.on_g37(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], G37]:
        """Get callback function for the node."""
        return visitor.on_g37
