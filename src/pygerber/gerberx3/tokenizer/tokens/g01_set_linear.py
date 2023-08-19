"""Wrapper for G01 mode set token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.state_enums import DrawMode
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class SetLinear(Token):
    """Wrapper for G01 mode set token.

    Sets linear/circular mode to linear.
    """

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing mode."""
        return (
            state.model_copy(
                update={
                    "draw_mode": DrawMode.Linear,
                },
            ),
            (),
        )

    def __str__(self) -> str:
        return "G01*"
