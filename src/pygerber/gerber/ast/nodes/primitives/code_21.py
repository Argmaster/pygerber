"""`pygerber.nodes.primitives.Code21` module contains definition of `Code21` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Code21(Node):
    """Represents code 21 macro primitive."""

    exposure: Expression
    width: Expression
    height: Expression
    center_x: Expression
    center_y: Expression
    rotation: Expression

    def visit(self, visitor: AstVisitor) -> Code21:
        """Handle visitor call."""
        return visitor.on_code_21(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Code21]:
        """Get callback function for the node."""
        return visitor.on_code_21
