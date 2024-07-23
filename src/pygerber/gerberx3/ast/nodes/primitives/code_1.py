"""`pygerber.nodes.primitives.Code1` module contains definition of `Code1` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import Field

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class Code1(Node):
    """Represents code 1 macro primitive."""

    exposure: Expression
    diameter: Expression
    center_x: Expression
    center_y: Expression
    rotation: Optional[Expression] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_code_1(self)
