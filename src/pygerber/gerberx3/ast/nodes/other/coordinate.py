"""`pygerber.nodes.other.Coordinate` module contains definition of `Coordinate`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class Coordinate(Node):
    """Represents Coordinate node."""


class CoordinateX(Coordinate):
    """Represents X Coordinate node."""

    value: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_coordinate_x(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_coordinate_x


class CoordinateY(Coordinate):
    """Represents Y Coordinate node."""

    value: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_coordinate_y(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_coordinate_y


class CoordinateI(Coordinate):
    """Represents I Coordinate node."""

    value: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_coordinate_i(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_coordinate_i


class CoordinateJ(Coordinate):
    """Represents J Coordinate node."""

    value: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_coordinate_j(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_coordinate_j
