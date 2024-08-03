"""`pygerber.nodes.properties.MO` module contains definition of `MO` class."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class UnitMode(Enum):
    """Unit mode enumeration."""

    IMPERIAL = "IN"
    """Imperial unit mode. In this mode inches are used to express lengths."""
    METRIC = "MM"
    """Metric unit mode. In this mode millimeters are used to express lengths."""


class MO(Node):
    """Represents MO Gerber extended command."""

    mode: UnitMode

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_mo(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_mo
