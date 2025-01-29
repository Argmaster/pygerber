"""`pygerber.nodes.aperture.ABclose` module contains definition of `ABclose` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class ABclose(Node):
    """Represents AB Gerber extended command."""

    def visit(self, visitor: AstVisitor) -> ABclose:
        """Handle visitor call."""
        return visitor.on_ab_close(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], ABclose]:
        """Get callback function for the node."""
        return visitor.on_ab_close
