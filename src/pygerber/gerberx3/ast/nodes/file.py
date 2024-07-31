"""`pygerber.gerberx3.ast.nodes.file` module contains definition of `File` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class File(Node):
    """AST node representing Gerber file."""

    nodes: list[Node]

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_file(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_file
