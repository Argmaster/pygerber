"""`pygerber.nodes.aperture.SR` module contains definition of `SR` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

from pygerber.gerberx3.ast.nodes.aperture.SR_close import SRclose
from pygerber.gerberx3.ast.nodes.aperture.SR_open import SRopen
from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.ast_visitor import AstVisitor


class SR(Node):
    """Represents SR Gerber extended command."""

    open: SRopen
    nodes: List[Node]
    close: SRclose

    def visit(self, visitor: AstVisitor) -> SR:
        """Handle visitor call."""
        return visitor.on_sr(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], SR]:
        """Get callback function for the node."""
        return visitor.on_sr
