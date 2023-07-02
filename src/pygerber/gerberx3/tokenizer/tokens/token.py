"""Base class for creating token classes."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyparsing import ParserElement, ParseResults
    from typing_extensions import Self


class Token:
    """Base class for creating token classes."""

    @classmethod
    def wrap(cls, expr: ParserElement) -> ParserElement:
        """Set parse result to be instance of this class."""
        return expr.set_parse_action(cls.new)

    @classmethod
    def new(cls, _string: str, _location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        return cls(**tokens.as_dict())
