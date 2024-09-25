"""`pygerber.nodes.properties.FS` module contains definition of `FS` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.enums import CoordinateNotation, Zeros

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class FS(Node):
    """Represents FS Gerber extended command."""

    zeros: Zeros
    coordinate_mode: CoordinateNotation

    x_integral: int
    x_decimal: int

    y_integral: int
    y_decimal: int

    def visit(self, visitor: AstVisitor) -> FS:
        """Handle visitor call."""
        return visitor.on_fs(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], FS]:
        """Get callback function for the node."""
        return visitor.on_fs
