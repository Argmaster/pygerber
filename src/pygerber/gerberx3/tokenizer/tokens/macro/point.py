"""Point wrapper token."""


from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.sequence_tools import unwrap


class Point(Expression):
    """Point wrapper token."""

    def __init__(
        self,
        x: Expression,
        y: Expression,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.x = unwrap(x)
        self.y = unwrap(y)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"{self.x},{self.y}"
