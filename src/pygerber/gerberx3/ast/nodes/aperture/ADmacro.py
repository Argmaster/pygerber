"""`pygerber.nodes.aperture.ADmacro` module contains definition of `AD` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List, Optional

from pydantic import Field

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.types import Double

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class ADmacro(Node):
    """Represents AD macro Gerber extended command."""

    aperture_identifier: str
    name: str
    params: Optional[List[Double]] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_ad_macro(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_ad_macro
