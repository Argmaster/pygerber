"""Wrapper for optional stop token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.parser.errors import ExitParsingProcessInterrupt
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_actions.draw_action import DrawAction
    from pygerber.gerberx3.parser.state import State


class M01OptionalStop(Token):
    """Wrapper for optional stop token."""

    def update_drawing_state(
        self,
        _state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawAction]]:
        """Exit drawing process."""
        raise ExitParsingProcessInterrupt

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return "M00*"