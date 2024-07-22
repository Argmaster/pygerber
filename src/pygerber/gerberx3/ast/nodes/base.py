"""`pygerber.gerberx3.ast.nodes.base` contains definition of `node` class."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from pygerber.vm.types.model import ModelType

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class Node(ModelType):
    """Base class for all nodes."""

    source: str
    location: int

    @abstractmethod
    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
