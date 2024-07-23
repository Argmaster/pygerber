"""`pygerber.nodes.primitives.Code6` module contains definition of `Code6` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


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

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_code_6(self)
