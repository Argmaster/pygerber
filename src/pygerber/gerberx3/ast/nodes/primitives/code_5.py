"""`pygerber.nodes.primitives.Code5` module contains definition of `Code5` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class Code5(Node):
    """Represents code 5 macro primitive."""

    exposure: Expression
    number_of_vertices: Expression
    center_x: Expression
    center_y: Expression
    diameter: Expression
    rotation: Expression

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_code_5(self)
