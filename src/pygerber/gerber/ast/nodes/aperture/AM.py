"""`pygerber.nodes.aperture.AM` module contains definition of `AM` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

from pygerber.gerber.ast.nodes.aperture.AM_close import AMclose
from pygerber.gerber.ast.nodes.aperture.AM_open import AMopen
from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class AM(Node):
    """Represents AM Gerber extended command."""

    open: AMopen
    primitives: List[Node]
    close: AMclose

    def visit(self, visitor: AstVisitor) -> AM:
        """Handle visitor call."""
        return visitor.on_am(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], AM]:
        """Get callback function for the node."""
        return visitor.on_am
