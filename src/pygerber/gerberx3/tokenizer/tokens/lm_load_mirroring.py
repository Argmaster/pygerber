"""Wrapper for load mirroring token."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.state_enums import Mirroring
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


class LoadMirroring(ExtendedCommandToken):
    """Wrapper for load mirroring token.

    Loads the mirror object transformation parameter.

    See section 4.9.3 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def __init__(
        self,
        string: str,
        location: int,
        mirroring: Mirroring,
    ) -> None:
        super().__init__(string, location)
        self.mirroring = mirroring

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        mirroring = Mirroring(tokens["mirroring"])
        return cls(string=string, location=location, mirroring=mirroring)

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

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().load_mirroring.pre_parser_visit_token(self, context)
        context.get_hooks().load_mirroring.on_parser_visit_token(self, context)
        context.get_hooks().load_mirroring.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"LM{self.mirroring.value}"
