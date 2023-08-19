"""Wrapper for set unit mode token."""
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


class UnitMode(Token):
    """Wrapper for set unit mode token.

    Sets the unit to mm or inch.
    """

    unit: Unit

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        unit: Unit = Unit(tokens["unit"])
        if unit == Unit.Inches:
            logging.warning(
                "Using metric units is recommended. Imperial units will be deprecated "
                "in future. (See 4.2.1 in Gerber Layer Format Specification)",
            )
        return cls(unit=unit)

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        if state.draw_units is not None:
            logging.warning(
                "Overriding coordinate format is illegal. "
                "(See 4.2.1 in Gerber Layer Format Specification)",
            )
        return (
            state.model_copy(
                update={
                    "draw_units": self.unit,
                },
            ),
            (),
        )

    def __str__(self) -> str:
        return f"%MO{self.unit.value}*%"
