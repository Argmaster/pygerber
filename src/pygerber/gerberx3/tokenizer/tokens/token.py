"""Base class for creating token classes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pyparsing import col, lineno

from pygerber.gerberx3.tokenizer.gerber_code import GerberCode

if TYPE_CHECKING:
    from pyparsing import ParserElement, ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class Token(GerberCode):
    """Base class for creating token classes."""

    @classmethod
    def wrap(cls, expr: ParserElement) -> ParserElement:
        """Set parse result to be instance of this class."""
        return expr.set_parse_action(cls.new)

    @classmethod
    def new(cls, string: str, location: int, _tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        return cls(string, location)

    def __init__(self, string: str, location: int) -> None:
        """Initialize token instance."""
        self.string = string
        self.location = location

    def __str__(self) -> str:
        return f"GerberCode::Token::{self.__class__.__qualname__}"

    def __repr__(self) -> str:
        """Return pretty representation of comment token."""
        return self.__str__()

    def get_debug_format(self) -> str:
        """Return debug formatted token object."""
        return super().__repr__()

    @classmethod
    def ensure_type(cls, thing: Any) -> Self:
        """Ensure that <thing> is a instance of NumericExpression.

        Raise TypeError otherwise.
        """
        if not isinstance(thing, cls):
            raise TypeError(thing)

        return thing

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        return state, ()

    def get_token_position(self) -> Position:
        """Get position of token."""
        return Position(
            lineno(self.location, self.string),
            col(self.location, self.string),
        )


@dataclass
class Position:
    """Position of token in text."""

    line: int
    column: int

    def __str__(self) -> str:
        return f"[line: {self.line}, col: {self.column}]"


class GerberX3Token(Token):
    """Base class for tokens which are part of Gerber X3 standard."""


class DeprecatedToken(Token):
    """Base class for tokens which are deprecated."""
