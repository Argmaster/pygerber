"""`pygerber.nodes.aperture.SR_close` module contains definition of `SRclose`
class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class SRclose(Node):
    """Represents SR Gerber extended command."""

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_sr_close(self)
