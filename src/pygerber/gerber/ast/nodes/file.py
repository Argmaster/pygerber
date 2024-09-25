"""`nodes.file` module contains definition of `File` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class File(Node):
    """The `File` node class represents a root of Gerber AST.

    It will be invalid for a File node to contain another File node.
    """

    nodes: List[Node]

    def visit(self, visitor: AstVisitor) -> File:
        """Handle visitor call."""
        return visitor.on_file(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], File]:
        """Get callback function for the node."""
        return visitor.on_file
