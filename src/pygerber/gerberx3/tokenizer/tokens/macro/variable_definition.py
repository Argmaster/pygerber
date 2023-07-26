"""Macro variable definition token."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.gerberx3.tokenizer.tokens.macro.variable_name import MacroVariableName
from pygerber.sequence_tools import unwrap

if TYPE_CHECKING:
    from typing_extensions import Self


class MacroVariableDefinition(Expression):
    """Wrapper for macro variable definition."""

    variable: MacroVariableName
    value: Expression

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        variable = unwrap(tokens["macro_variable_name"])
        value = unwrap(tokens["value"])
        return cls(variable=variable, value=value)

    def __str__(self) -> str:
        return f"{self.variable}={self.value}*"
