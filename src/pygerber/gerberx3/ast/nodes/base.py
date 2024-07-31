"""`pygerber.gerberx3.ast.nodes.base` contains definition of `node` class."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Callable

from pydantic import Field

from pygerber.gerberx3.ast.nodes.model import ModelType

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class Node(ModelType):
    """Base class for all nodes."""

    source: str = Field(repr=False, exclude=True)
    location: int = Field(repr=False)

    @abstractmethod
    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""

    @abstractmethod
    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
