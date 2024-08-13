"""`pygerber.nodes.properties.AS` module contains definition of `AS` class."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class AxisCorrespondence(Enum):
    """Represents axis correspondence."""

    AX_BY = "AXBY"
    AY_BX = "AYBX"


class AS(Node):
    """Represents AS Gerber extended command."""

    correspondence: AxisCorrespondence

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_as(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_as
