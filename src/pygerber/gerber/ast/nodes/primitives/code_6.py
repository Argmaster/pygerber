"""`pygerber.nodes.primitives.Code6` module contains definition of `Code6` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Code6(Node):
    """Represents code 6 macro primitive."""

    center_x: Expression
    center_y: Expression
    outer_diameter: Expression
    ring_thickness: Expression
    gap_between_rings: Expression
    max_ring_count: Expression
    crosshair_thickness: Expression
    crosshair_length: Expression
    rotation: Expression

    def visit(self, visitor: AstVisitor) -> Code6:
        """Handle visitor call."""
        return visitor.on_code_6(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Code6]:
        """Get callback function for the node."""
        return visitor.on_code_6
