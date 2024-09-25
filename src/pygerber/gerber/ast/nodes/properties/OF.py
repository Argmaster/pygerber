"""`pygerber.nodes.properties.OF` module contains definition of `OF` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from pydantic import Field

from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class OF(Node):
    """Represents OF Gerber extended command."""

    a_offset: Optional[float] = Field(default=None)
    b_offset: Optional[float] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> OF:
        """Handle visitor call."""
        return visitor.on_of(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], OF]:
        """Get callback function for the node."""
        return visitor.on_of
