"""`pygerber.nodes.properties.MO` module contains definition of `MO` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.enums import UnitMode

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class MO(Node):
    """Represents MO Gerber extended command."""

    mode: UnitMode

    def visit(self, visitor: AstVisitor) -> MO:
        """Handle visitor call."""
        return visitor.on_mo(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], MO]:
        """Get callback function for the node."""
        return visitor.on_mo
