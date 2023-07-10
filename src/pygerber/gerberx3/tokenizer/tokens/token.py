"""Base class for creating token classes."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pyparsing import Group

if TYPE_CHECKING:
    from pyparsing import ParserElement, ParseResults
    from typing_extensions import Self


class Token:
    """Base class for creating token classes."""

    def __init__(self) -> None:
        """Initialize token object."""
        logging.debug("Constructing token %s", self.__class__.__qualname__)

    @classmethod
    def wrap(cls, expr: ParserElement, *, use_group: bool = True) -> ParserElement:
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
        return cls(**dict(tokens))

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"<TOKEN {self.__class__.__qualname__}>"

    def __repr__(self) -> str:
        """Return pretty representation of comment token."""
        string = str(self)
        repr_string = f"<TOKEN {self.__class__.__qualname__}>"

        if repr_string == string:
            return repr_string

        return f"<{self.__class__.__qualname__} {string!r}>"

    def __getitem__(self, _: int) -> Self:
        """Index return self."""
        return self
