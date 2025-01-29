"""`pygerber.nodes.other.CoordinateJ` module contains definition of `CoordinateJ`
class which represent Jxx...x packed coordinates.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.other.coordinate import Coordinate

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class CoordinateJ(Coordinate):
    """Represents J Coordinate node."""

    def visit(self, visitor: AstVisitor) -> CoordinateJ:
        """Handle visitor call."""
        return visitor.on_coordinate_j(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], CoordinateJ]:
        """Get callback function for the node."""
        return visitor.on_coordinate_j
