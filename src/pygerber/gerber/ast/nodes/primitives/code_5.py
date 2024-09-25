"""`pygerber.nodes.primitives.Code5` module contains definition of `Code5` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Code5(Node):
    """Represents code 5 macro primitive."""

    exposure: Expression
    number_of_vertices: Expression
    center_x: Expression
    center_y: Expression
    diameter: Expression
    rotation: Expression

    def visit(self, visitor: AstVisitor) -> Code5:
        """Handle visitor call."""
        return visitor.on_code_5(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Code5]:
        """Get callback function for the node."""
        return visitor.on_code_5
