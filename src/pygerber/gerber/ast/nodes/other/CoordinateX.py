"""`pygerber.nodes.other.CoordinateX` module contains definition of `CoordinateX`
class which represent Xxx...x packed coordinates.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.other.coordinate import Coordinate

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class CoordinateX(Coordinate):
    """Represents X Coordinate node."""

    def visit(self, visitor: AstVisitor) -> CoordinateX:
        """Handle visitor call."""
        return visitor.on_coordinate_x(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], CoordinateX]:
        """Get callback function for the node."""
        return visitor.on_coordinate_x
