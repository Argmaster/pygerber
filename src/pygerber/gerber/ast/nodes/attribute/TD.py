"""`pygerber.nodes.attribute.TD` module contains definition of `TD` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from pydantic import Field

from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class TD(Node):
    """Represents TD Gerber extended command."""

    name: Optional[str] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> TD:
        """Handle visitor call."""
        return visitor.on_td(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], TD]:
        """Get callback function for the node."""
        return visitor.on_td
