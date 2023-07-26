"""Wrapper for aperture select token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class StepRepeatBegin(Token):
    """Wrapper for SR begin token.

    Opens an SR statement and starts block accumulation.
    """

    x_repeat: float
    y_repeat: float
    x_step: float
    y_step: float

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        x_repeat = float(tokens["x_repeat"])
        y_repeat = float(tokens["y_repeat"])
        x_step = float(tokens["x_step"])
        y_step = float(tokens["y_step"])
        return cls(
            x_repeat=x_repeat,
            y_repeat=y_repeat,
            x_step=x_step,
            y_step=y_step,
        )

    def __str__(self) -> str:
        return f"SRX{self.x_repeat}Y{self.y_repeat}I{self.x_step}J{self.y_step}*"


class StepRepeatEnd(Token):
    """Wrapper for SR end token.

    Ends step and repeat statement.
    """

    def __str__(self) -> str:
        return "SR*"
