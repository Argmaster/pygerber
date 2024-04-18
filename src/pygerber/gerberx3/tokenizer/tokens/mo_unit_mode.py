"""Wrapper for set unit mode token."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.state_enums import Unit
from pygerber.gerberx3.tokenizer.tokens.bases.extended_command import (
    ExtendedCommandToken,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class UnitMode(ExtendedCommandToken):
    """Wrapper for set unit mode token.

    Sets the unit to mm or inch.
    """

    def __init__(self, string: str, location: int, unit: Unit) -> None:
        super().__init__(string, location)
        self.unit = unit

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        unit: Unit = Unit(tokens["unit"])
        return cls(string=string, location=location, unit=unit)

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        if self.unit == Unit.Inches:
            logging.warning(
                "Detected use of imperial units. Using metric units is recommended. "
                "Imperial units will be deprecated in future. "
                "(See 4.2.1 in Gerber Layer Format Specification)",
            )
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

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().unit_mode.pre_parser_visit_token(self, context)
        context.get_hooks().unit_mode.on_parser_visit_token(self, context)
        context.get_hooks().unit_mode.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"MO{self.unit.value}"
