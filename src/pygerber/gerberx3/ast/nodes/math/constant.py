"""`pygerber.nodes.math.constant` module contains definition of `Constant` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.math.expression import Expression
from pygerber.gerberx3.ast.nodes.types import Double

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.ast_visitor import AstVisitor


class Constant(Expression):
    """Represents math expression constant."""

    constant: Double

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_constant(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_constant
