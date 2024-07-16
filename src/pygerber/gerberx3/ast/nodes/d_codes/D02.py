"""`pygerber.nodes.d_codes.D02` module contains definition of `D02` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.other.coordinate import Coordinate

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class D02(Node):
    """Represents D02 Gerber command."""

    x: Coordinate
    y: Coordinate

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_d02(self)
