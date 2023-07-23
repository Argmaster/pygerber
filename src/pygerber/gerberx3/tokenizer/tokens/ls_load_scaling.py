"""Wrapper for load scaling token."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_actions.draw_action import DrawAction
    from pygerber.gerberx3.parser.state import State


class LoadScaling(Token):
    """Wrapper for load scaling token.

    Loads the scaling object transformation parameter.
    """

    scaling: Decimal

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        scaling = Decimal(tokens["scaling"])
        return cls(scaling=scaling)

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawAction]]:
        """Set drawing polarity."""
        return (
            state.model_copy(
                update={
                    "scaling": self.scaling,
                },
                deep=True,
            ),
            (),
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"LS{self.scaling}*"
