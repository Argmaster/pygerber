"""Wrapper for flash operation token."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Iterator, Optional, Sequence

from pygerber.common.position import Position
from pygerber.gerberx3.tokenizer.tokens.bases.token import Token
from pygerber.gerberx3.tokenizer.tokens.bases.token_accessor import TokenAccessor

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self


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
        threshold = 10
        if len(self.tokens) > threshold:
            return self._find_closest_token_binary(pos, parent)

        return self._find_closest_token_linear(pos, parent)

    def _find_closest_token_binary(
        self,
        pos: Position,
        parent: TokenAccessor,
    ) -> TokenAccessor:
        left = 0
        right = len(self.tokens) - 1
        center = (left + right) // 2

        while left <= right:
            center = (left + right) // 2
            token = self.tokens[center]
            token_pos = token.get_token_position()

            if token_pos < pos:
                left = center + 1
            elif token_pos > pos:
                right = center - 1
            else:
                break

        while ((token := self.tokens[center]).get_token_position()) > pos:
            center -= 1

        return TokenAccessor(
            self.tokens[center],
            parent,
            self.tokens,
            center,
        )

    def _find_closest_token_linear(
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
                    self.tokens,
                    i,
                )

            prev_token = token

        return TokenAccessor(prev_token, parent, self.tokens, i)

    def __iter__(self) -> Iterator[Token]:
        for token in self.tokens:
            yield from token

    def __len__(self) -> int:
        return self.tokens.__len__()
