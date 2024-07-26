"""`pygerber.nodes.properties.MO` module contains definition of `MO` class."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class UnitMode(Enum):
    """Unit mode enumeration."""

    INCH = "IN"
    MILLIMETER = "MM"


class MO(Node):
    """Represents MO Gerber extended command."""

    mode: UnitMode

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_mo(self)
