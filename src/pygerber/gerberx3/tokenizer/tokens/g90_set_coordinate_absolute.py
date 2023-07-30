"""Wrapper for G90 token."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class SetAbsoluteNotation(Token):
    """Wrapper for G90 token.

    Set the `Coordinate format` to `Absolute notation`.

    This historic code performs a function handled by the FS command. See 4.1. Very
    rarely used nowadays. Deprecated in 2012.

    SPEC: `2023.03` SECTION: `8.1`
    """

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        if state.coordinate_parser is not None:
            logging.warning(
                "Overriding coordinate format is illegal."
                "(See 4.2.2 in Gerber Layer Format Specification)",
            )
        return (
            state.model_copy(deep=True),
            (),
        )

    def __str__(self) -> str:
        return "G90*"
