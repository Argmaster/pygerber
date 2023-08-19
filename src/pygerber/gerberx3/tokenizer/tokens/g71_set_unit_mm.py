"""Wrapper for G71 token."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.state_enums import Unit
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class SetUnitMillimeters(Token):
    """Wrapper for G71 token.

    Set the `Unit` to millimeter.

    This historic codes perform a function handled by the MO command. See 4.2.1.
    Sometimes used. Deprecated in 2012
    """

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        if state.draw_units is not None:
            logging.warning(
                "Overriding coordinate format is illegal. "
                "(See 4.2.1 in Gerber Layer Format Specification)",
            )
        return (
            state.model_copy(
                update={
                    "draw_units": Unit.Millimeters,
                },
            ),
            (),
        )

    def __str__(self) -> str:
        return "G71*"
