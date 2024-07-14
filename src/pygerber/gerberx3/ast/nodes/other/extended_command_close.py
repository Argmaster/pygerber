"""`pygerber.nodes.other.ExtendedCommandClose` module contains definition of
`ExtendedCommandClose` class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class ExtendedCommandClose(Node):
    """Represents ExtendedCommandClose node."""

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_extended_command_close(self)
