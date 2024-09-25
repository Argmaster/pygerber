"""`pygerber.nodes.m_codes.M01` module contains definition of `M01` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class M01(Node):
    """Represents M01 Gerber command."""

    def visit(self, visitor: AstVisitor) -> M01:
        """Handle visitor call."""
        return visitor.on_m01(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], M01]:
        """Get callback function for the node."""
        return visitor.on_m01
