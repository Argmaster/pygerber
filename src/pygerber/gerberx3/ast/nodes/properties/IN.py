"""`pygerber.nodes.properties.IN` module contains definition of `IN` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pydantic import Field

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class IN(Node):
    """Represents IN Gerber extended command."""

    name: str = Field(default="")

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_in(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_in