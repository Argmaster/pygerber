"""Wrapper for G70 token."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import DNNSelectAperture
from pygerber.warnings import warn_deprecated_code

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class G54SelectAperture(DNNSelectAperture):
    """Wrapper for G54DNN token.

    Select aperture.

    This historic code optionally precedes an aperture selection Dnn command. It has no
    effect. Sometimes used. Deprecated in 2012.

    See section 8.1.1 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        warn_deprecated_code("G54", "8.1")
        return super().update_drawing_state(state, _backend)

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().prepare_select_aperture.pre_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().prepare_select_aperture.on_parser_visit_token(self, context)
        context.get_hooks().prepare_select_aperture.post_parser_visit_token(
            self,
            context,
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}G54{self.aperture_id}"
