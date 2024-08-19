"""`pygerber.nodes.aperture.AM` module contains definition of `AM` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.aperture.AM_close import AMclose
from pygerber.gerberx3.ast.nodes.aperture.AM_open import AMopen
from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class AM(Node):
    """Represents AM Gerber extended command."""

    open: AMopen
    primitives: list[Node]
    close: AMclose

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_am(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_am
