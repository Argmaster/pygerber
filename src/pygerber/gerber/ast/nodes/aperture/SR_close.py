"""`pygerber.nodes.aperture.SR_close` module contains definition of `SRclose`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class SRclose(Node):
    """Represents SR Gerber extended command."""

    def visit(self, visitor: AstVisitor) -> SRclose:
        """Handle visitor call."""
        return visitor.on_sr_close(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], SRclose]:
        """Get callback function for the node."""
        return visitor.on_sr_close
