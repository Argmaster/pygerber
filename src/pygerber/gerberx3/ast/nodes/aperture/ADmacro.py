"""`pygerber.nodes.aperture.ADmacro` module contains definition of `AD` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from pydantic import Field

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class ADmacro(Node):
    """Represents AD macro Gerber extended command."""

    aperture_identifier: str
    name: str
    params: Optional[List[str]] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_ad_macro(self)
