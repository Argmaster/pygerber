"""The `node_finder` module contains `NodeFinder` class, which can quickly find AST
nodes by their location in source code.
"""

from __future__ import annotations

from typing import Optional, Sequence

from pydantic import BaseModel, Field

from pygerber.gerber.ast.ast_visitor import AstVisitor
from pygerber.gerber.ast.nodes import AB, AM, SR, File, Node


class ZeroBasedPosition(BaseModel):
    """Zero-based position in source code."""

    line: int = Field(ge=0)
    column: int = Field(ge=0)

    def to_one_based(self) -> OneBasedPosition:
        """Convert zero-based position to one-based position."""
        return OneBasedPosition(line=self.line + 1, column=self.column + 1)


class OneBasedPosition(BaseModel):
    """One-based position in source code."""

    line: int = Field(ge=1)
    column: int = Field(ge=1)


class NodeFinder(AstVisitor):
    """The `NodeFinder` class can quickly find AST nodes by their location
    in source code.
    """

    def __init__(self, ast: File) -> None:
        self.ast = ast

    def find_node(self, location: OneBasedPosition) -> Optional[Node]:
        """Find node closest to the given location."""
        self.location = location
        self.return_node: Optional[Node] = self.ast
        self.on_file(self.ast)
        return self.return_node

    def on_file(self, node: File) -> File:
        """Handle `File` node."""
        if len(node.nodes) == 0:
            return node

        if len(node.nodes) == 1:
            self.return_node = node.nodes[0]
            return node

        self.return_node = self._bin_search(node.nodes)

        return node

    def on_am(self, node: AM) -> AM:
        """Handle `AM` root node."""
        self._bin_search([node.open, *node.primitives, node.close])
        return node

    def on_ab(self, node: AB) -> AB:
        """Handle `AB` root node."""
        self._bin_search([node.open, *node.nodes, node.close])
        return node

    def on_sr(self, node: SR) -> SR:
        """Handle `SR` root node."""
        self._bin_search([node.open, *node.nodes, node.close])
        return node

    def _bin_search(self, nodes: Sequence[Node]) -> Optional[Node]:  # noqa: PLR0911
        if len(nodes) == 1:
            self.return_node = nodes[0]
            source_info = self.return_node.source_info
            if source_info is not None and self.location.column < source_info.column:
                self.return_node = None
                return None

            self.return_node.visit(self)
            return self.return_node

        center_index = len(nodes) // 2
        center_node = nodes[center_index]
        source_info = center_node.source_info

        if source_info is None:
            return self.ast

        if self.location.line == source_info.line:
            if self.location.column == source_info.column:
                return self._bin_search(nodes=[center_node])

            if self.location.column < source_info.column:
                return self._bin_search(nodes=nodes[:center_index])

            return self._bin_search(nodes=nodes[center_index:])

        if self.location.line < source_info.line:
            return self._bin_search(nodes=nodes[:center_index])

        return self._bin_search(nodes=nodes[center_index:])
