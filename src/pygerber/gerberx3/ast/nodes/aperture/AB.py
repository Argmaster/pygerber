"""`pygerber.nodes.aperture.AB` module contains definition of `AB` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.aperture.AB_close import ABclose
from pygerber.gerberx3.ast.nodes.aperture.AB_open import ABopen
from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class AB(Node):
    """Represents AB Gerber extended command."""

    open: ABopen
    nodes: list[Node]
    close: ABclose

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_ab(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_ab
