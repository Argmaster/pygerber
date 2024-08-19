"""`pygerber.nodes.load.LM` module contains definition of `LM` class."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class Mirroring(Enum):
    """Mirroring enum."""

    None_ = "N"
    X = "X"
    Y = "Y"
    XY = "XY"


class LM(Node):
    """Represents LM Gerber extended command."""

    mirroring: Mirroring

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_lm(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_lm