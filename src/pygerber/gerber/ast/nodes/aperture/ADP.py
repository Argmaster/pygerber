"""`pygerber.nodes.aperture.ADP` module contains definition of `AD` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from pydantic import Field

from pygerber.gerber.ast.nodes.aperture.AD import AD
from pygerber.gerber.ast.nodes.types import Double, Integer

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class ADP(AD):
    """Represents AD polygon Gerber extended command."""

    outer_diameter: Double
    vertices: Integer
    rotation: Optional[Double] = Field(default=None)
    hole_diameter: Optional[Double] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> ADP:
        """Handle visitor call."""
        return visitor.on_adp(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], ADP]:
        """Get callback function for the node."""
        return visitor.on_adp
