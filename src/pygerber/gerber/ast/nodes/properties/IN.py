"""`pygerber.nodes.properties.IN` module contains definition of `IN` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pydantic import Field

from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class IN(Node):
    """Represents IN Gerber extended command."""

    name: str = Field(default="")

    def visit(self, visitor: AstVisitor) -> IN:
        """Handle visitor call."""
        return visitor.on_in(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], IN]:
        """Get callback function for the node."""
        return visitor.on_in
