"""Wrapper for G74 token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class SetMultiQuadrantMode(Token):
    """Wrapper for G74 token.

    In multi quadrant mode the arc is allowed to extend over more than 90°.
    To avoid ambiguity between 0° and 360° arcs the following relation must hold:

    0° < A ≤360°, where A is the arc angle

    If the start point of the arc is equal to the
    end point, the arc is a full circle of 360°.

    0° ≤A ≤90°, where A is the arc angle

    angleIf the start point of the arc is equal to the end point, the arc has length
    zero, i.e. it covers 0°. A separate operation is required for each quadrant. A
    minimum of four operations is required for a full circle.
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
                    "is_multi_quadrant": True,
                },
            ),
            (),
        )

    def __str__(self) -> str:
        return "G75*"
