"""`pygerber.nodes.aperture.AMopen` module contains definition of `AMopen` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class AMopen(Node):
    """Represents AM Gerber extended command."""

    name: str

    def visit(self, visitor: AstVisitor) -> AMopen:
        """Handle visitor call."""
        return visitor.on_am_open(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], AMopen]:
        """Get callback function for the node."""
        return visitor.on_am_open
