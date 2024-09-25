"""`pygerber.nodes.aperture.ADmacro` module contains definition of `AD` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List, Optional

from pydantic import Field

from pygerber.gerber.ast.nodes.aperture.AD import AD
from pygerber.gerber.ast.nodes.types import Double

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class ADmacro(AD):
    """Represents AD macro Gerber extended command."""

    name: str
    params: Optional[List[Double]] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> ADmacro:
        """Handle visitor call."""
        return visitor.on_ad_macro(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], ADmacro]:
        """Get callback function for the node."""
        return visitor.on_ad_macro
