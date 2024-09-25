"""`pygerber.nodes.g_codes.G04` module contains definition of `G04` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Invalid(Node):
    """Represents G04 Gerber command."""

    string: str

    def visit(self, visitor: AstVisitor) -> Invalid:
        """Handle visitor call."""
        return visitor.on_invalid(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Invalid]:
        """Get callback function for the node."""
        return visitor.on_invalid
