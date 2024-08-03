"""Wrapper for set unit mode token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.state_enums import Unit
from pygerber.gerberx3.tokenizer.tokens.bases.extended_command import (
    ExtendedCommandToken,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class UnitMode(ExtendedCommandToken):
    """Wrapper for set unit mode token.

    Sets the unit to mm or inch.
    """

    def __init__(self, string: str, location: int, unit: Unit) -> None:
        super().__init__(string, location)
        self.unit = unit

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        unit: Unit = Unit(tokens["unit"])
        return cls(string=string, location=location, unit=unit)

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().unit_mode.pre_parser_visit_token(self, context)
        context.get_hooks().unit_mode.on_parser_visit_token(self, context)
        context.get_hooks().unit_mode.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"MO{self.unit.value}"
