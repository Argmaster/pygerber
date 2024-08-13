"""`pygerber.nodes.properties.SF` module contains definition of `SF` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pydantic import Field

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class SF(Node):
    """Represents SF Gerber extended command."""

    a_scale: float = Field(default=1.0)
    b_scale: float = Field(default=1.0)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_sf(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_sf
