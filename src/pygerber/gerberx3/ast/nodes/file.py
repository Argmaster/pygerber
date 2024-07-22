"""`pygerber.gerberx3.ast.nodes.file` module contains definition of `File` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class File(Node):
    """AST node representing Gerber file."""

    commands: list[Node]

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_file(self)
