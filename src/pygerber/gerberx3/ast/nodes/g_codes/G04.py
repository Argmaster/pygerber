"""`pygerber.nodes.g_codes.G04` module contains definition of `G04` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from pydantic import Field

from pygerber.gerberx3.ast.nodes.g_codes.G import G

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.ast_visitor import AstVisitor


class G04(G):
    """Represents G04 Gerber command."""

    string: Optional[str] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> G04:
        """Handle visitor call."""
        return visitor.on_g04(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], G04]:
        """Get callback function for the node."""
        return visitor.on_g04
