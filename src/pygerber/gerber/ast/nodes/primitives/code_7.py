"""`pygerber.nodes.primitives.Code7` module contains definition of `Code7` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Code7(Node):
    """Represents code 7 macro primitive."""

    center_x: Expression
    center_y: Expression
    outer_diameter: Expression
    inner_diameter: Expression
    gap_thickness: Expression
    rotation: Expression

    def visit(self, visitor: AstVisitor) -> Code7:
        """Handle visitor call."""
        return visitor.on_code_7(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Code7]:
        """Get callback function for the node."""
        return visitor.on_code_7
