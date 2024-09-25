"""`pygerber.nodes.load.LP` module contains definition of `LP` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.enums import Polarity

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class LP(Node):
    """Represents LP Gerber extended command."""

    polarity: Polarity

    def visit(self, visitor: AstVisitor) -> LP:
        """Handle visitor call."""
        return visitor.on_lp(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], LP]:
        """Get callback function for the node."""
        return visitor.on_lp
