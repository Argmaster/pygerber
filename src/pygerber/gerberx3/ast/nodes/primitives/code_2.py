"""`pygerber.nodes.primitives.Code2` module contains definition of `Code2` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class Code2(Node):
    """Represents code 2 macro primitive."""

    exposure: Expression
    width: Expression
    start_x: Expression
    start_y: Expression
    end_x: Expression
    end_y: Expression
    rotation: Expression

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_code_2(self)
