"""`pygerber.nodes.load.LR` module contains definition of `LR` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class LR(Node):
    """Represents LR Gerber extended command."""

    rotation: float

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_lr(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_lr
