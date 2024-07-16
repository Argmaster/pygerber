"""`pygerber.nodes.other.Coordinate` module contains definition of `Coordinate`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class Coordinate(Node):
    """Represents Coordinate node."""

    type: Literal["X", "Y", "I", "J"]
    value: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_coordinate(self)
