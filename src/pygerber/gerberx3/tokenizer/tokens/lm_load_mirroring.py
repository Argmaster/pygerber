"""Wrapper for load mirroring token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.gerberx3.state_enums import Mirroring
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class LoadMirroring(Token):
    """Wrapper for load mirroring token.

    Loads the mirror object transformation parameter.
    """

    mirroring: Mirroring

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        mirroring = Mirroring(tokens["mirroring"])
        return cls(mirroring=mirroring)

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        return (
            state.model_copy(
                update={
                    "mirroring": self.mirroring,
                },
            ),
            (),
        )

    def __str__(self) -> str:
        return f"LM{self.mirroring.value}*"
