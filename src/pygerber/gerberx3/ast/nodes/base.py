"""`pygerber.gerberx3.ast.nodes.base` contains definition of `node` class."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Callable, Optional

import pyparsing as pp
from pydantic import Field

from pygerber.gerberx3.ast.nodes.model import ModelType

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.ast_visitor import AstVisitor


class SourceInfo(ModelType):
    """Source information for the node."""

    source: str
    location: int
    length: int

    @pp.cached_property
    def line(self) -> int:
        """Get the line number of the start location within the string; the first line
        is line 1, newlines start new rows.
        """
        return pp.lineno(self.location, self.source)

    @pp.cached_property
    def column(self) -> int:
        """Get the column number of the start location within the string; the first
        column is column 1, newlines reset the column number to 1.
        """
        return pp.col(self.location, self.source)


class Node(ModelType):
    """Base class for all nodes."""

    source_info: Optional[SourceInfo] = Field(default=None, repr=False, exclude=True)
    source: str = Field(default="", repr=False, exclude=True)
    location: int = Field(default=0, repr=False, exclude=True)

    @abstractmethod
    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""

    @abstractmethod
    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""

    def __len__(self) -> int:
        """Get the length of token in source code."""
        if self.source_info is None:
            return 0
        return self.source_info.length
