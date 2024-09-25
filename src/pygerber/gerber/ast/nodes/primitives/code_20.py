"""`pygerber.nodes.primitives.Code20` module contains definition of `Code20` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Code20(Node):
    """Represents code 20 macro primitive."""

    exposure: Expression
    width: Expression
    start_x: Expression
    start_y: Expression
    end_x: Expression
    end_y: Expression
    rotation: Expression

    def visit(self, visitor: AstVisitor) -> Code20:
        """Handle visitor call."""
        return visitor.on_code_20(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Code20]:
        """Get callback function for the node."""
        return visitor.on_code_20
