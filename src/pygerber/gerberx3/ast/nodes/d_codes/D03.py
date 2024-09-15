"""`pygerber.nodes.d_codes.D03` module contains definition of `D03` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from pydantic import Field

from pygerber.gerberx3.ast.nodes.d_codes.D import D
from pygerber.gerberx3.ast.nodes.other.coordinate import (
    CoordinateX,
    CoordinateY,
)

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.ast_visitor import AstVisitor


class D03(D):
    """Represents D03 Gerber command."""

    x: Optional[CoordinateX] = Field(default=None)
    y: Optional[CoordinateY] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> D03:
        """Handle visitor call."""
        return visitor.on_d03(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], D03]:
        """Get callback function for the node."""
        return visitor.on_d03
