"""`pygerber.nodes.primitives.Code2` module contains definition of `Code2` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Code2(Node):
    """Represents code 2 macro primitive."""

    exposure: Expression
    width: Expression
    start_x: Expression
    start_y: Expression
    end_x: Expression
    end_y: Expression
    rotation: Expression

    def visit(self, visitor: AstVisitor) -> Code2:
        """Handle visitor call."""
        return visitor.on_code_2(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Code2]:
        """Get callback function for the node."""
        return visitor.on_code_2
