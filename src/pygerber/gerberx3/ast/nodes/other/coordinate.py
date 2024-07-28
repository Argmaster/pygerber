"""`pygerber.nodes.other.Coordinate` module contains definition of `Coordinate`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class Coordinate(Node):
    """Represents Coordinate node."""

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_coordinate(self)


class CoordinateX(Coordinate):
    """Represents X Coordinate node."""

    value: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_coordinate_x(self)


class CoordinateY(Coordinate):
    """Represents Y Coordinate node."""

    value: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_coordinate_y(self)


class CoordinateI(Coordinate):
    """Represents I Coordinate node."""

    value: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_coordinate_i(self)


class CoordinateJ(Coordinate):
    """Represents J Coordinate node."""

    value: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_coordinate_j(self)
