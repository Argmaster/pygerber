"""Wrapper for G01 mode set token."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.state_enums import DrawMode
from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class SetLinear(CommandToken):
    """Wrapper for G01 mode set token.

    Sets linear/circular mode to linear.
    See:
    -   section 4.8 of The Gerber Layer Format Specification Revision 2020.09 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2020_09.html
    -   section 4.7 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing mode."""
        return (
            state.model_copy(
                update={
                    "draw_mode": DrawMode.Linear,
                },
            ),
            (),
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().set_linear.pre_parser_visit_token(self, context)
        context.get_hooks().set_linear.on_parser_visit_token(self, context)
        context.get_hooks().set_linear.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}G01"
