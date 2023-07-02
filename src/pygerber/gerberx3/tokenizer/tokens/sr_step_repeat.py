"""Wrapper for aperture select token."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.token import Token


class StepRepeatBegin(Token):
    """Wrapper for SR begin token.

    Opens an SR statement and starts block accumulation.
    """

    def __init__(self, x_repeat: str, y_repeat: str, x_step: str, y_step: str) -> None:
        """Initialize token object."""
        super().__init__()
        self.x_repeat = float(x_repeat)
        self.y_repeat = float(y_repeat)
        self.x_step = float(x_step)
        self.y_step = float(y_step)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"SRX{self.x_repeat}Y{self.y_repeat}I{self.x_step}J{self.y_step}*"


class StepRepeatEnd(Token):
    """Wrapper for SR end token.

    Ends step and repeat statement.
    """

    def __init__(self) -> None:
        """Initialize token object."""
        super().__init__()

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return "SR*"
