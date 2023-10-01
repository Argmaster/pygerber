"""Wrapper for flash operation token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, List, Optional, Sequence, Tuple

from pygerber.common.position import Position
from pygerber.gerberx3.tokenizer.tokens.bases.token import Token
from pygerber.gerberx3.tokenizer.tokens.bases.token_accessor import TokenAccessor

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
        tokens: Sequence[Token],
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

    def find_closest_token(
        self,
        pos: Position,
        parent: Optional[TokenAccessor] = None,
    ) -> TokenAccessor:
        """Find token closest to specified position."""
        if parent is None:
            parent = TokenAccessor(self)

        token_accessor = self._find_closest_token(pos, parent)
        token = token_accessor.token

        if token and isinstance(token, TokenGroup):
            token_accessor = token.find_closest_token(pos, token_accessor)

        return token_accessor

    def _find_closest_token(
        self,
        pos: Position,
        parent: TokenAccessor,
    ) -> TokenAccessor:
        i = 0
        search_pos = pos
        token = prev_token = self.tokens[i]

        for i, token in enumerate(self.tokens):
            token_pos = token.get_token_position()
            if token_pos > search_pos:
                return TokenAccessor(
                    prev_token,
                    parent,
                    self.tokens[:i],
                    self.tokens[i + 1 :],
                )

            prev_token = token

        return TokenAccessor(prev_token, parent, self.tokens[:i], self.tokens[i + 1 :])
