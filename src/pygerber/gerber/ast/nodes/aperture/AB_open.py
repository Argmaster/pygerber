"""`pygerber.nodes.aperture.ABopen` module contains definition of `ABopen` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.types import ApertureIdStr

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class ABopen(Node):
    """Represents AB Gerber extended command."""

    aperture_id: ApertureIdStr

    def visit(self, visitor: AstVisitor) -> ABopen:
        """Handle visitor call."""
        return visitor.on_ab_open(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], ABopen]:
        """Get callback function for the node."""
        return visitor.on_ab_open
