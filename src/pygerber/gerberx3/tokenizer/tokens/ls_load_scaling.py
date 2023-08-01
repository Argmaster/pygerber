"""Wrapper for load scaling token."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class LoadScaling(Token):
    """Wrapper for load scaling token.

    ### LS Command: Scaling Graphics State Parameter

    The `LS` command is employed to establish the scaling graphics state parameter.

    Functionality:
    - The command dictates the scale factor utilized during object creation.
    - The aperture undergoes scaling, anchored at its origin. It's crucial to note that
        this origin might not always align with its geometric center.

    Usage and Persistence:
    - The `LS` command can be invoked multiple times within a single file.
    - Once set, the object scaling retains its value unless a subsequent `LS` command
        modifies it.
    - The scaling gets adjusted based on the specific value mentioned in the command and
        doesn't accumulate with the preceding scale factor.

    The LS command was introduced in revision 2016.12.

    SPEC: `2023.03` SECTION: `4.9.5`
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
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        return (
            state.model_copy(
                update={
                    "scaling": self.scaling,
                },
            ),
            (),
        )

    def __str__(self) -> str:
        return f"LS{self.scaling}*"
