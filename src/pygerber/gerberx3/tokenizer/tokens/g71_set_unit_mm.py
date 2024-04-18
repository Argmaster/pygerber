"""Wrapper for G71 token."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.state_enums import Unit
from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken
from pygerber.warnings import warn_deprecated_code

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class SetUnitMillimeters(CommandToken):
    """Wrapper for G71 token.

    Set the `Unit` to millimeter.

    This historic codes perform a function handled by the MO command.
    Sometimes used. Deprecated in 2012

    See section 4.2.1 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        warn_deprecated_code("G71", "8.1")
        if state.draw_units is not None:
            logging.warning(
                "Overriding coordinate units is illegal. "
                "(See section 4.2.2 of The Gerber Layer Format Specification "
                "Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html)",
            )
        return (
            state.model_copy(
                update={
                    "draw_units": Unit.Millimeters,
                },
            ),
            (),
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().set_unit_millimeters.pre_parser_visit_token(self, context)
        context.get_hooks().set_unit_millimeters.on_parser_visit_token(self, context)
        context.get_hooks().set_unit_millimeters.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}G71"
