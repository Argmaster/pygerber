"""Base class for creating token classes."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pyparsing import Group

from pygerber.common.frozen_general_model import FrozenGeneralModel

if TYPE_CHECKING:
    from pyparsing import ParserElement, ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class Token(FrozenGeneralModel):
    """Base class for creating token classes."""

    @classmethod
    def wrap(
        cls,
        expr: ParserElement,
        *,
        use_group: bool = True,
    ) -> ParserElement:
        """Set parse result to be instance of this class."""
        expr = expr.set_parse_action(cls.new)

        if use_group:
            return Group(expr)

        return expr

    @classmethod
    def new(cls, _string: str, _location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        return cls.from_tokens(**dict(tokens))

    @classmethod
    def from_tokens(cls, **_tokens: Any) -> Self:
        """Initialize token object."""
        return cls()

    def __str__(self) -> str:
        return f"<TOKEN {self.__class__.__qualname__}>"

    def __repr__(self) -> str:
        """Return pretty representation of comment token."""
        string = str(self)
        repr_string = f"<TOKEN {self.__class__.__qualname__}>"

        if repr_string == string:
            return repr_string

        return f"<{self.__class__.__qualname__} {string!r}>"

    def get_debug_format(self) -> str:
        """Return debug formatted token object."""
        return super().__repr__()

    def __getitem__(self, _: int) -> Self:
        """Index return self."""
        return self

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        return state, ()


class GerberX3Token(Token):
    """Base class for tokens which are part of Gerber X3 standard."""


class DeprecatedToken(Token):
    """Base class for tokens which are deprecated."""
