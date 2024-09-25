"""`pygerber.nodes.other.Coordinate` module contains definition of `Coordinate`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.types import PackedCoordinateStr

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Coordinate(Node):
    """Represents Coordinate node."""

    value: PackedCoordinateStr


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
