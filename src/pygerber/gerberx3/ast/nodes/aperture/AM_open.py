"""`pygerber.nodes.aperture.AMopen` module contains definition of `AMopen` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class AMopen(Node):
    """Represents AM Gerber extended command."""

    name: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_am_open(self)
