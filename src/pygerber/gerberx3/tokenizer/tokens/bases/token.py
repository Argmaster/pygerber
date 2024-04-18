"""Base class for creating token classes."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, Iterable, Iterator, Optional, Tuple

from pyparsing import col, lineno

from pygerber.common.position import Position
from pygerber.gerberx3.linter import diagnostic
from pygerber.gerberx3.tokenizer.tokens.bases.gerber_code import GerberCode
from pygerber.gerberx3.tokenizer.tokens.bases.token_accessor import TokenAccessor

if TYPE_CHECKING:
    from pyparsing import ParserElement, ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Token(GerberCode):
    """Base class for creating Gerber token classes."""

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
        """Ensure that <thing> is a instance of this class.

        Raise TypeError otherwise.
        """
        if not isinstance(thing, cls):
            raise TypeError(thing)

        return thing

    def parser2_visit_token(
        self,
        context: Parser2Context,
    ) -> None:
        """Update drawing state for Gerber AST parser, version 2."""

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        return state, ()

    def get_token_position(self) -> Position:
        """Get position of token."""
        return self._token_position

    @cached_property
    def _token_position(self) -> Position:
        return Position(
            lineno(self.location, self.string),
            col(self.location, self.string),
        )

    def get_hover_message(self, state: State) -> str:
        """Return language server hover message."""
        ref_doc = "\n".join(s.strip() for s in str(self.__doc__).split("\n"))
        op_specific_extra = self.get_state_based_hover_message(state)
        return (
            "```gerber\n"
            f"{self.get_gerber_code_one_line_pretty_display()}"
            "\n"
            "```"
            "\n"
            "---"
            "\n"
            f"{op_specific_extra}\n"
            "\n"
            "---"
            "\n"
            f"{ref_doc}"
        )

    def get_state_based_hover_message(
        self,
        state: State,  # noqa: ARG002
    ) -> str:
        """Return operation specific extra information about token."""
        return ""

    def find_closest_token(
        self,
        pos: Position,  # noqa: ARG002
        parent: Optional[TokenAccessor] = None,
    ) -> TokenAccessor:
        """Find token closest to specified position."""
        return TokenAccessor(self, parent)

    def get_gerber_code_one_line_pretty_display(self) -> str:
        """Get gerber code represented by this token."""
        return self.get_gerber_code()

    def get_token_diagnostics(self) -> Iterable[diagnostic.Diagnostic]:
        """Get diagnostics for this token."""
        return
        yield  # type: ignore[unreachable]

    def get_token_end_position(self) -> Position:
        """Get position of the end of the token."""
        s = str(self)
        first, *_ = s.split("\n")
        lines_offset = 0
        column_offset = len(first)
        return self.get_token_position().offset(lines_offset, column_offset)

    def __iter__(self) -> Iterator[Token]:
        yield self

    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Token):
            return NotImplemented
        return id(__value) == id(self)
