"""Wrapper for aperture select token."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class BeginRegion(CommandToken):
    """Wrapper for G36 token.

    Starts a region statement which creates a region by defining its contours.

    See section 4.10 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        if state.is_region:
            logging.warning("Starting region within a region is not allowed.")

        return (
            state.model_copy(
                update={
                    "is_region": True,
                    "region_boundary_points": [],
                },
            ),
            (),
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().begin_region.pre_parser_visit_token(self, context)
        context.get_hooks().begin_region.on_parser_visit_token(self, context)
        context.get_hooks().begin_region.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}G36"
