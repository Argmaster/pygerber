"""`pygerber.nodes.other.ExtendedCommandOpen` module contains definition of
`ExtendedCommandOpen` class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class ExtendedCommandOpen(Node):
    """Represents ExtendedCommandOpen node."""

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_extended_command_open(self)
