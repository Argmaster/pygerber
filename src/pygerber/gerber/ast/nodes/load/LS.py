"""`pygerber.nodes.load.LS` module contains definition of `LS` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.types import Double

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class LS(Node):
    """Represents LS Gerber extended command."""

    scale: Double

    def visit(self, visitor: AstVisitor) -> LS:
        """Handle visitor call."""
        return visitor.on_ls(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], LS]:
        """Get callback function for the node."""
        return visitor.on_ls
