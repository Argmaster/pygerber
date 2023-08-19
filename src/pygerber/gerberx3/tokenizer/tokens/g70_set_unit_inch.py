"""Wrapper for G70 token."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.gerberx3.state_enums import Unit
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class SetUnitInch(Token):
    """Wrapper for G70 token.

    Set the `Unit` to inch.

    This historic codes perform a function handled by the MO command. See 4.2.1.
    Sometimes used. Deprecated in 2012
    """

    @classmethod
    def from_tokens(cls, **_tokens: Any) -> Self:
        """Initialize token object."""
        logging.warning(
            "Using metric units is recommended. Imperial units will be deprecated "
            "in future. (See 4.2.1 in Gerber Layer Format Specification)",
        )
        return cls()

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
                    "draw_units": Unit.Inches,
                },
            ),
            (),
        )

    def __str__(self) -> str:
        return "G70*"
