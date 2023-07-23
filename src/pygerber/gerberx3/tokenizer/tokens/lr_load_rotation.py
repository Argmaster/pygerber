"""Wrapper for load rotation token."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_actions.draw_action import DrawAction
    from pygerber.gerberx3.parser.state import State


class LoadRotation(Token):
    """Wrapper for load rotation token.

    Loads the rotation object transformation parameter.
    """

    rotation: Decimal

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        rotation = Decimal(tokens["rotation"])
        return cls(rotation=rotation)

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawAction]]:
        """Set drawing polarity."""
        return (
            state.model_copy(
                update={
                    "rotation": self.rotation,
                },
                deep=True,
            ),
            (),
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"LR{self.rotation}*"
