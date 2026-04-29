"""`pygerber.nodes.aperture.SR_open` module contains definition of `SRopen` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from pydantic import Field

from pygerber.gerber.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class SRRepeatCountError(ValueError):
    """Raised when SR repeat count is invalid."""

    def __init__(self, axis: str, value: Optional[str] = None) -> None:
        message = (
            f"SR {axis} repeat count must be an integer greater than or equal to 1"
        )
        if value is not None:
            message = f"{message}, got {value!r}"
        super().__init__(message)


class SRopen(Node):
    """Represents SR Gerber extended command."""

    x: Optional[str] = Field(default=None)
    y: Optional[str] = Field(default=None)
    i: Optional[str] = Field(default=None)
    j: Optional[str] = Field(default=None)

    def _repeat_count(self, value: Optional[str], axis: str) -> int:
        if value is None:
            return 1

        try:
            repeats = int(value)
        except ValueError as exc:
            raise SRRepeatCountError(axis, value) from exc

        if repeats < 1:
            raise SRRepeatCountError(axis, value)
        return repeats

    @property
    def x_repeats(self) -> int:
        """Get number of repeats in X axis."""
        return self._repeat_count(self.x, "X")

    @property
    def y_repeats(self) -> int:
        """Get number of repeats in Y axis."""
        return self._repeat_count(self.y, "Y")

    @property
    def x_delta(self) -> float:
        """Get X step-and-repeat offset."""
        return 0 if self.i is None else float(self.i)

    @property
    def y_delta(self) -> float:
        """Get Y step-and-repeat offset."""
        return 0 if self.j is None else float(self.j)

    def visit(self, visitor: AstVisitor) -> SRopen:
        """Handle visitor call."""
        return visitor.on_sr_open(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], SRopen]:
        """Get callback function for the node."""
        return visitor.on_sr_open
