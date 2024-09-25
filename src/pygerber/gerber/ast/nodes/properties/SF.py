"""`pygerber.nodes.properties.SF` module contains definition of `SF` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pydantic import Field

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.types import Double

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class SF(Node):
    """Represents SF Gerber extended command."""

    a_scale: Double = Field(default=1.0)
    b_scale: Double = Field(default=1.0)

    def visit(self, visitor: AstVisitor) -> SF:
        """Handle visitor call."""
        return visitor.on_sf(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], SF]:
        """Get callback function for the node."""
        return visitor.on_sf
