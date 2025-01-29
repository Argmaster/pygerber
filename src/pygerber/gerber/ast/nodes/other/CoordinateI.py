"""`pygerber.nodes.other.CoordinateI` module contains definition of `CoordinateI`
class which represent Ixx...x packed coordinates.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.other.coordinate import Coordinate

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class CoordinateI(Coordinate):
    """Represents I Coordinate node."""

    def visit(self, visitor: AstVisitor) -> CoordinateI:
        """Handle visitor call."""
        return visitor.on_coordinate_i(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], CoordinateI]:
        """Get callback function for the node."""
        return visitor.on_coordinate_i
