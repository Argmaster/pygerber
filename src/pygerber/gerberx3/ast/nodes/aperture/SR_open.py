"""`pygerber.nodes.aperture.SR_open` module contains definition of `SRopen` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from pydantic import Field

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.ast_visitor import AstVisitor


class SRopen(Node):
    """Represents SR Gerber extended command."""

    x: Optional[str] = Field(default=None)
    y: Optional[str] = Field(default=None)
    i: Optional[str] = Field(default=None)
    j: Optional[str] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_sr_open(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_sr_open
