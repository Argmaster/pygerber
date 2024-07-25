"""`pygerber.nodes.properties.FS` module contains definition of `FS` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.other.coordinate import Coordinate

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class FS(Node):
    """Represents FS Gerber extended command."""

    x: Coordinate
    y: Coordinate
    zeros: str
    coordinate_mode: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_fs(self)
