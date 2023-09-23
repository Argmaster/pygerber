"""Wrapper for flash operation token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, List, Tuple

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class TokenGroup(Token):
    """Token consisting of multiple nested tokens."""

    def __init__(
        self,
        string: str,
        location: int,
        tokens: List[Token],
    ) -> None:
        super().__init__(string, location)
        self.tokens = tokens

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """

        def _() -> Iterable[Token]:
            for token in tokens.as_list():
                if isinstance(token, Token):
                    yield token

        return cls(
            string=string,
            location=location,
            tokens=list(_()),
        )

    def update_drawing_state(
        self,
        state: State,
        backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set coordinate parser."""
        draw_commands: List[DrawCommand] = []

        for token in self.tokens:
            state, result_commands = token.update_drawing_state(state, backend)
            draw_commands.extend(result_commands)

        return (
            state,
            draw_commands,
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        return endline.join(t.get_gerber_code(indent) for t in self.tokens)

    def __str__(self) -> str:
        prefix = super().__str__()
        tokens = ", ".join(str(t) for t in self.tokens)
        return f"{prefix}[{tokens}]"
