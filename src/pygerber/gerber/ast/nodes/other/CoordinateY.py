"""`pygerber.nodes.other.CoordinateY` module contains definition of `CoordinateY`
class which represent Yxx...x packed coordinates.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.other.coordinate import Coordinate

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class CoordinateY(Coordinate):
    """Represents Y Coordinate node."""

    def visit(self, visitor: AstVisitor) -> CoordinateY:
        """Handle visitor call."""
        return visitor.on_coordinate_y(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], CoordinateY]:
        """Get callback function for the node."""
        return visitor.on_coordinate_y
