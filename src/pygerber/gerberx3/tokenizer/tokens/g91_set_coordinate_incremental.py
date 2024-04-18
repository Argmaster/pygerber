"""Wrapper for G91 token."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken
from pygerber.warnings import warn_deprecated_code

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class SetIncrementalNotation(CommandToken):
    """Wrapper for G91 token.

    Set the `Coordinate format` to `Incremental notation`.

    This historic code performs a function handled by the FS command. See 4.1. Very
    rarely used nowadays. Deprecated in 2012.

    See section 8.1 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        warn_deprecated_code("G91", "8.1")
        if state.coordinate_parser is not None:
            logging.warning(
                "Overriding coordinate format is illegal. "
                "(See section 4.2.2 of The Gerber Layer Format Specification "
                "Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html)",
            )

        msg = "Incremental notation not supported."
        raise NotImplementedError(msg)

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().set_coordinate_incremental.pre_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().set_coordinate_incremental.on_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().set_coordinate_incremental.post_parser_visit_token(
            self,
            context,
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}G91"
