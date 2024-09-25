"""`pygerber.nodes.properties.IR` module contains definition of `IR` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class IR(Node):
    """Represents IR Gerber extended command."""

    rotation_degrees: int

    def visit(self, visitor: AstVisitor) -> IR:
        """Handle visitor call."""
        return visitor.on_ir(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], IR]:
        """Get callback function for the node."""
        return visitor.on_ir
