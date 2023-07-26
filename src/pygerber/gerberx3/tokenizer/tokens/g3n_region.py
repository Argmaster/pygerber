"""Wrapper for aperture select token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class BeginRegion(Token):
    """Wrapper for G36 token.

    Starts a region statement which creates a region by defining its contours.
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
                    "is_region": True,
                },
                deep=True,
            ),
            (),
        )

    def __str__(self) -> str:
        return "G36*"


class EndRegion(Token):
    """Wrapper for G37 token.

    Ends the region statement.
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
                    "is_region": False,
                },
                deep=True,
            ),
            (),
        )

    def __str__(self) -> str:
        return "G37*"
