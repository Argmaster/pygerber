"""`pygerber.nodes.primitives.Code4` module contains definition of `Code4` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.math.expression import Expression
from pygerber.gerber.ast.nodes.math.point import Point

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Code4(Node):
    """Represents code 4 macro primitive."""

    exposure: Expression
    number_of_points: Expression
    start_x: Expression
    start_y: Expression
    points: List[Point]
    rotation: Expression

    def visit(self, visitor: AstVisitor) -> Code4:
        """Handle visitor call."""
        return visitor.on_code_4(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Code4]:
        """Get callback function for the node."""
        return visitor.on_code_4
