"""`pygerber.nodes.primitives.Code0` module contains definition of `Code0` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Code0(Node):
    """Represents code 0 macro primitive."""

    string: str

    def visit(self, visitor: AstVisitor) -> Code0:
        """Handle visitor call."""
        return visitor.on_code_0(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Code0]:
        """Get callback function for the node."""
        return visitor.on_code_0
