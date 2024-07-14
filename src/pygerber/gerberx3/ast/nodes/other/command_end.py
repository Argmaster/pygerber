"""`pygerber.nodes.other.command_end` module contains definition of `CommandEnd`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class CommandEnd(Node):
    """Represents CommandEnd node."""

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_command_end(self)
