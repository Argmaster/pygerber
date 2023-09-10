"""Wrapper for aperture select token."""
from __future__ import annotations

import logging
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
        if state.is_region:
            logging.warning("Starting region within a region is not allowed.")

        return (
            state.model_copy(
                update={
                    "is_region": True,
                    "region_boundary_points": [],
                },
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
        backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        if not state.is_region:
            logging.warning("Ending region which was not started.")

        if len(state.region_boundary_points) == 0:
            logging.warning("Created region with no boundaries.")

        draw_command = backend.get_draw_region_cls()(
            backend,
            state.polarity.to_region_variant(),
            state.region_boundary_points,
        )

        return (
            state.model_copy(
                update={
                    "is_region": False,
                    "region_boundary_points": [],
                },
            ),
            (draw_command,),
        )

    def __str__(self) -> str:
        return "G37*"
