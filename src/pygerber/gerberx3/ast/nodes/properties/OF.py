"""`pygerber.nodes.properties.OF` module contains definition of `OF` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class OF(Node):
    """Represents OF Gerber extended command."""

    a_offset: Optional[float]
    b_offset: Optional[float]

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_of(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_of
