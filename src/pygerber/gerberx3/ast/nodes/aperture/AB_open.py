"""`pygerber.nodes.aperture.ABopen` module contains definition of `ABopen` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class ABopen(Node):
    """Represents AB Gerber extended command."""

    aperture_identifier: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_ab_open(self)
