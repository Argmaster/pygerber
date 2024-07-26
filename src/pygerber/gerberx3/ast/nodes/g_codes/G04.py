"""`pygerber.nodes.g_codes.G04` module contains definition of `G04` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import Field

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class G04(Node):
    """Represents G04 Gerber command."""

    string: Optional[str] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_g04(self)
