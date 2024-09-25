"""`pygerber.nodes.math.constant` module contains definition of `Constant` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast.nodes.math.expression import Expression
from pygerber.gerber.ast.nodes.types import Double

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class Constant(Expression):
    """Represents math expression constant."""

    constant: Double

    def visit(self, visitor: AstVisitor) -> Constant:
        """Handle visitor call."""
        return visitor.on_constant(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], Constant]:
        """Get callback function for the node."""
        return visitor.on_constant

    def __hash__(self) -> int:
        return hash(self.constant)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Constant):
            return self.constant == value.constant

        return NotImplemented
