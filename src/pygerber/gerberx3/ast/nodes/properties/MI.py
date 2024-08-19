"""`pygerber.nodes.properties.MI` module contains definition of `MI` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pydantic import Field

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class MI(Node):
    """Represents MI Gerber extended command."""

    a_mirroring: int = Field(default=0)
    b_mirroring: int = Field(default=0)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_mi(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_mi