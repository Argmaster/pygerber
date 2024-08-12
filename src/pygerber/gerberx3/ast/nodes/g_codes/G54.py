"""`pygerber.nodes.g_codes.G54` module contains definition of `G54` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.d_codes.Dnn import Dnn

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class G54(Node):
    """Represents G54 Gerber command."""

    dnn: Dnn

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_g54(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_g54
