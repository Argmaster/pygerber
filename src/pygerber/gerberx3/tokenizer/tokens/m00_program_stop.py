"""Wrapper for program stop token."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.parser.errors import ExitParsingProcessInterrupt
from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class M00ProgramStop(CommandToken):
    """Wrapper for program stop token.

    See section 8.1.1 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def update_drawing_state(
        self,
        _state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Exit drawing process."""
        raise ExitParsingProcessInterrupt

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().program_stop.pre_parser_visit_token(self, context)
        context.get_hooks().program_stop.on_parser_visit_token(self, context)
        context.get_hooks().program_stop.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}M00"
