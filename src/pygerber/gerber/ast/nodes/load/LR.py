"""`pygerber.nodes.load.LR` module contains definition of `LR` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.types import Double

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class LR(Node):
    """Represents LR Gerber extended command."""

    rotation: Double

    def visit(self, visitor: AstVisitor) -> LR:
        """Handle visitor call."""
        return visitor.on_lr(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], LR]:
        """Get callback function for the node."""
        return visitor.on_lr
