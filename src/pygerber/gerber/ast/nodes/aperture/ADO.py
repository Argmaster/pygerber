"""`pygerber.nodes.aperture.ADO` module contains definition of `AD` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from pydantic import Field

from pygerber.gerber.ast.nodes.aperture.AD import AD
from pygerber.gerber.ast.nodes.types import Double

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class ADO(AD):
    """Represents AD obround Gerber extended command."""

    width: Double
    height: Double
    hole_diameter: Optional[Double] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> ADO:
        """Handle visitor call."""
        return visitor.on_ado(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], ADO]:
        """Get callback function for the node."""
        return visitor.on_ado
