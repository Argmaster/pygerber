"""`pygerber.nodes.aperture.AB` module contains definition of `AB` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

from pygerber.gerber.ast.nodes.aperture.AB_close import ABclose
from pygerber.gerber.ast.nodes.aperture.AB_open import ABopen
from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class AB(Node):
    """Represents AB Gerber extended command."""

    open: ABopen
    nodes: List[Node]
    close: ABclose

    def visit(self, visitor: AstVisitor) -> AB:
        """Handle visitor call."""
        return visitor.on_ab(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], AB]:
        """Get callback function for the node."""
        return visitor.on_ab
