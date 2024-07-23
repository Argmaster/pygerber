"""`pygerber.nodes.primitives.Code21` module contains definition of `Code21` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class Code21(Node):
    """Represents code 21 macro primitive."""

    exposure: Expression
    width: Expression
    height: Expression
    center_x: Expression
    center_y: Expression
    rotation: Expression

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_code_21(self)
