"""Wrapper for load rotation token."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class LoadRotation(Token):
    """Wrapper for load rotation token.

    ### LR Command: Rotation Graphics State Parameter

    The `LR` command is utilized to configure the rotation graphics state parameter.

    Functionality:
    - This command specifies the rotation angle to be applied when crafting objects.
    - The aperture is rotated centered on its origin, which might either coincide with
        or differ from its geometric center.

    Usage and Persistence:
    - The `LR` command can be invoked numerous times throughout a file.
    - Once defined, the object rotation retains its configuration unless overridden by
        an ensuing `LR` command.
    - Rotation is strictly determined by the exact value mentioned in the command and
        doesn't integrate with any prior rotation values.

    The LR command was introduced in revision 2016.12.

    SPEC: `2023.03` SECTION: `4.9.4`
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
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        return (
            state.model_copy(
                update={
                    "rotation": self.rotation,
                },
            ),
            (),
        )

    def __str__(self) -> str:
        return f"LR{self.rotation}*"
