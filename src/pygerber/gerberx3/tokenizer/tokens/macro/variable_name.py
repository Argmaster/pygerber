"""Macro variable use token."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext
from pygerber.gerberx3.tokenizer.tokens.macro.numeric_expression import (
    NumericExpression,
)
from pygerber.sequence_tools import unwrap

if TYPE_CHECKING:
    from typing_extensions import Self


class MacroVariableName(NumericExpression):
    """Wrapper for macro variable use."""

    name: str

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        name = unwrap(tokens["macro_variable_name"])
        return cls(name=name)

    def evaluate_numeric(self, macro_context: MacroContext, _state: State) -> Offset:
        """Evaluate numeric value of this macro expression."""
        return macro_context.variables[self.name]

    def __str__(self) -> str:
        return self.name
