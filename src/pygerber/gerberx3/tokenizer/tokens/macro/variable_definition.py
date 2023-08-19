"""Macro variable definition token."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext
from pygerber.gerberx3.tokenizer.tokens.macro.numeric_expression import (
    NumericExpression,
)
from pygerber.gerberx3.tokenizer.tokens.macro.variable_name import MacroVariableName
from pygerber.sequence_tools import unwrap

if TYPE_CHECKING:
    from typing_extensions import Self


class MacroVariableDefinition(Expression):
    """Wrapper for macro variable definition."""

    variable: MacroVariableName
    value: NumericExpression

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        variable = unwrap(tokens["macro_variable_name"])
        value = unwrap(tokens["value"])
        return cls(variable=variable, value=value)

    def evaluate(
        self,
        macro_context: MacroContext,
        state: State,
        handle: PrivateApertureHandle,
    ) -> None:
        """Evaluate macro expression."""
        name = self.variable.name
        value = self.value.evaluate_numeric(macro_context, state)
        macro_context.variables[name] = value

        return super().evaluate(macro_context, state, handle)

    def __str__(self) -> str:
        return f"{self.variable}={self.value}*"
