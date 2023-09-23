"""Wrapper for aperture select token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self


class BlockApertureBegin(Token):
    """Wrapper for AB begin token.

    Opens a block aperture statement and assigns its aperture number.

    See section 4.7 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def __init__(self, string: str, location: int, identifier: ApertureID) -> None:
        super().__init__(string, location)
        self.identifier = identifier

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        return cls(string, location, ApertureID(tokens["aperture_identifier"]))

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

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}AB{self.identifier.get_gerber_code()}*"


class BlockApertureEnd(Token):
    """Wrapper for AB end token.

    Ends block aperture statement.
    """

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}AB*"
