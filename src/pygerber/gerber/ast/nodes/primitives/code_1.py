"""`pygerber.nodes.primitives.Code1` module contains definition of `Code1` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from pydantic import Field

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Code1(Node):
    """Represents code 1 macro primitive."""

    exposure: Expression
    diameter: Expression
    center_x: Expression
    center_y: Expression
    rotation: Optional[Expression] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> Code1:
        """Handle visitor call."""
        return visitor.on_code_1(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Code1]:
        """Get callback function for the node."""
        return visitor.on_code_1
