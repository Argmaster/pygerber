"""`pygerber.nodes.load.LM` module contains definition of `LM` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.enums import Mirroring

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class LM(Node):
    """Represents LM Gerber extended command."""

    mirroring: Mirroring

    def visit(self, visitor: AstVisitor) -> LM:
        """Handle visitor call."""
        return visitor.on_lm(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], LM]:
        """Get callback function for the node."""
        return visitor.on_lm
