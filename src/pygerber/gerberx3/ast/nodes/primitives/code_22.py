"""`pygerber.nodes.primitives.Code22` module contains definition of `Code22` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.math.expression import Expression

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class Code22(Node):
    """Represents code 22 macro primitive."""

    exposure: Expression
    width: Expression
    height: Expression
    x_lower_left: Expression
    y_lower_left: Expression
    rotation: Expression

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_code_22(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_code_22