"""`pygerber.nodes.properties.IR` module contains definition of `IR` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class IR(Node):
    """Represents IR Gerber extended command."""

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_ir(self)
