"""Wrapper for load scaling token."""

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


class LoadScaling(ExtendedCommandToken):
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

    See section 4.9.5 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def __init__(
        self,
        string: str,
        location: int,
        scaling: Decimal,
    ) -> None:
        super().__init__(string, location)
        self.scaling = scaling

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        scaling = Decimal(str(tokens["scaling"]))
        return cls(string=string, location=location, scaling=scaling)

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

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().load_scaling.pre_parser_visit_token(self, context)
        context.get_hooks().load_scaling.on_parser_visit_token(self, context)
        context.get_hooks().load_scaling.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"LS{self.scaling}"
