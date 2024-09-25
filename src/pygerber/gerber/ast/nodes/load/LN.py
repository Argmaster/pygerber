"""`pygerber.nodes.load.LN` module contains definition of `LN` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class LN(Node):
    """Represents LN Gerber extended command."""

    name: str

    def visit(self, visitor: AstVisitor) -> LN:
        """Handle visitor call."""
        return visitor.on_ln(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], LN]:
        """Get callback function for the node."""
        return visitor.on_ln
