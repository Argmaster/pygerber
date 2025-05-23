"""`pygerber.nodes.properties.AS` module contains definition of `AS` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.enums import AxisCorrespondence

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class AS(Node):
    """Represents AS Gerber extended command."""

    correspondence: AxisCorrespondence

    def visit(self, visitor: AstVisitor) -> AS:
        """Handle visitor call."""
        return visitor.on_as(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], AS]:
        """Get callback function for the node."""
        return visitor.on_as
