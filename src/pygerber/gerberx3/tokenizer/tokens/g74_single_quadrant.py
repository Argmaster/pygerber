"""Wrapper for G74 token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken
from pygerber.warnings import warn_deprecated_code

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class SetSingleQuadrantMode(CommandToken):
    """Wrapper for G74 token.

    Sets single quadrant mode - Rarely used, and then typically without effect.
    Deprecated in 2020.

    In single quadrant mode the arc is not allowed to extend over more than 90°.

    See:
    -   section 4.7 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    -   section 8.1.10 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        warn_deprecated_code("G74", "8.1.10")
        return (
            state.model_copy(
                update={
                    "is_multi_quadrant": False,
                },
            ),
            (),
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}G74"
