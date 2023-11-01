"""Wrapper for aperture select token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pydantic_core import CoreSchema, core_schema

from pygerber.gerberx3.parser.errors import ApertureNotDefinedError
from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken
from pygerber.gerberx3.tokenizer.tokens.bases.gerber_code import GerberCode

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class DNNSelectAperture(CommandToken):
    """## 4.6 Current Aperture (Dnn).

    The command Dnn (nn≥10) sets the current aperture graphics state parameter. The syntax is:

    ```ebnf
    Dnn = 'D unsigned_integer '*';
    ```

    - `D` - Command code.
    - `<aperture number>` - The aperture number (integer ≥10). An aperture with that number must be in the apertures dictionary.

    D-commands 0 to 9 are reserved and cannot be used for apertures. The D01 and D03
    commands use the current aperture to create track and flash graphical objects.

    ---

    ## Example

    ```gerber
    D10*
    ```

    ---

    See section 4.6 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=75)

    """  # noqa: E501

    def __init__(self, string: str, location: int, aperture_id: ApertureID) -> None:
        super().__init__(string, location)
        self.aperture_id = aperture_id

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        return cls(
            string=string,
            location=location,
            aperture_id=ApertureID(tokens["aperture_identifier"]),
        )

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set current aperture."""
        if self.aperture_id not in state.apertures:
            raise ApertureNotDefinedError(self.aperture_id)
        return (
            state.model_copy(
                update={
                    "current_aperture": state.apertures[self.aperture_id],
                },
            ),
            (),
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}{self.aperture_id.get_gerber_code(indent, endline)}"


class ApertureID(str, GerberCode):
    """Aperture ID wrapper."""

    __slots__ = ()

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Generate the pydantic-core schema."""
        return core_schema.no_info_after_validator_function(cls, handler(str))

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{self}"
