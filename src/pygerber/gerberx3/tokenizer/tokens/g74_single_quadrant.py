"""Wrapper for G74 token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class SetSingleQuadrantMode(Token):
    """Wrapper for G74 token.

    Sets single quadrant mode - Rarely used, and then typically without effect.
    Deprecated in 2020. (Spec. 8.1.10).

    In single quadrant mode the arc is not allowed to extend over more than 90°.
    """

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        return (
            state.model_copy(
                update={
                    "is_multi_quadrant": False,
                },
            ),
            (),
        )

    def __str__(self) -> str:
        return "G74*"
