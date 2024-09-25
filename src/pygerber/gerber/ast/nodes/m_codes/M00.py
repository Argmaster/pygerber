"""`pygerber.nodes.m_codes.M00` module contains definition of `M00` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class M00(Node):
    """Represents M00 Gerber command."""

    def visit(self, visitor: AstVisitor) -> M00:
        """Handle visitor call."""
        return visitor.on_m00(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], M00]:
        """Get callback function for the node."""
        return visitor.on_m00
