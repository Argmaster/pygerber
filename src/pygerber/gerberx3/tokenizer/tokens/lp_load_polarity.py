"""Wrapper for load polarity token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.gerberx3.state_enums import Polarity
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class LoadPolarity(Token):
    """Wrapper for load polarity token.

    Loads the scale object transformation parameter.
    """

    polarity: Polarity

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        polarity = Polarity(tokens["polarity"])
        return cls(polarity=polarity)

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        return (
            state.model_copy(
                update={
                    "polarity": self.polarity,
                },
            ),
            (),
        )

    def __str__(self) -> str:
        return f"LP{self.polarity.value}*"
