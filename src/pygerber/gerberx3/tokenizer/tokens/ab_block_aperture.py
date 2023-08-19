"""Wrapper for aperture select token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class BlockApertureBegin(Token):
    """Wrapper for AB begin token.

    Opens a block aperture statement and assigns its aperture number.
    """

    identifier: ApertureID

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        identifier = ApertureID(tokens["aperture_identifier"])
        return cls(identifier=identifier)

    def update_drawing_state(
        self,
        state: State,
        backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        handle = backend.create_aperture_handle(self.identifier)
        with handle:
            # Must be included to initialize drawing target.
            pass
        frozen_handle = handle.get_public_handle()

        new_aperture_dict = {**state.apertures}
        new_aperture_dict[self.identifier] = frozen_handle

        return (
            state.model_copy(
                update={
                    "apertures": new_aperture_dict,
                },
            ),
            (),
        )

    def __str__(self) -> str:
        return f"AB{self.identifier}*"


class BlockApertureEnd(Token):
    """Wrapper for AB end token.

    Ends block aperture statement.
    """

    @classmethod
    def from_tokens(cls, **_tokens: Any) -> Self:
        """Initialize token object."""
        return cls()

    def __str__(self) -> str:
        return "AB*"
