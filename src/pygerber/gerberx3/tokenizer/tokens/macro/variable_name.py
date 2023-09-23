"""Macro variable use token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext
from pygerber.gerberx3.tokenizer.tokens.macro.numeric_expression import (
    NumericExpression,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self


class MacroVariableName(NumericExpression):
    """Wrapper for macro variable use."""

    def __init__(self, string: str, location: int, name: str) -> None:
        super().__init__(string, location)
        self.name = name

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        name = str(tokens["macro_variable_name"][0])
        return cls(string=string, location=location, name=name)

    def evaluate_numeric(self, macro_context: MacroContext, _state: State) -> Offset:
        """Evaluate numeric value of this macro expression."""
        return macro_context.variables[self.name]

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return indent + self.name
