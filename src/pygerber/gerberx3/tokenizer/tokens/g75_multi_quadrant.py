"""Wrapper for G74 token."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class SetMultiQuadrantMode(CommandToken):
    """Wrapper for G75 token.

    In multi quadrant mode the arc is allowed to extend over more than 90°.
    To avoid ambiguity between 0° and 360° arcs the following relation must hold:

    0° < A ≤360°, where A is the arc angle

    If the start point of the arc is equal to the
    end point, the arc is a full circle of 360°.

    0° ≤A ≤90°, where A is the arc angle

    angleIf the start point of the arc is equal to the end point, the arc has length
    zero, i.e. it covers 0°. A separate operation is required for each quadrant. A
    minimum of four operations is required for a full circle.

    See:
    -   section 4.8 of The Gerber Layer Format Specification Revision 2020.09 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2020_09.html
    -   section 4.7 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    -   section 8.1.10 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        return (
            state.model_copy(
                update={
                    "is_multi_quadrant": True,
                },
            ),
            (),
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().set_multi_quadrant_mode.pre_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().set_multi_quadrant_mode.on_parser_visit_token(self, context)
        context.get_hooks().set_multi_quadrant_mode.post_parser_visit_token(
            self,
            context,
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}G75"
