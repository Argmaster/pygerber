"""`pygerber.nodes.primitives.Code7` module contains definition of `Code7` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class Code7(Node):
    """Represents code 7 macro primitive."""

    center_x: Expression
    center_y: Expression
    outer_diameter: Expression
    inner_diameter: Expression
    gap_thickness: Expression
    rotation: Expression

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_code_7(self)
