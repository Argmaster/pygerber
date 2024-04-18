"""Wrapper for load rotation token."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.bases.extended_command import (
    ExtendedCommandToken,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class LoadRotation(ExtendedCommandToken):
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

    See section 4.9.4 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def __init__(
        self,
        string: str,
        location: int,
        rotation: Decimal,
    ) -> None:
        super().__init__(string, location)
        self.rotation = rotation

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        rotation = Decimal(str(tokens["rotation"]))
        return cls(string=string, location=location, rotation=rotation)

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

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().load_rotation.pre_parser_visit_token(self, context)
        context.get_hooks().load_rotation.on_parser_visit_token(self, context)
        context.get_hooks().load_rotation.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"LR{self.rotation}"
