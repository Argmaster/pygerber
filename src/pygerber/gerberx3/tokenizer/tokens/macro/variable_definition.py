"""Macro variable definition token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.macro.element import Element
from pygerber.sequence_tools import unwrap

if TYPE_CHECKING:
    from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
    from pygerber.gerberx3.tokenizer.tokens.macro.variable_name import MacroVariableName


class MacroVariableDefinition(Element):
    """Wrapper for macro variable definition."""

    def __init__(self, variable: MacroVariableName, value: Expression) -> None:
        """Initialize token object."""
        super().__init__()
        self.variable = unwrap(variable)
        self.value = unwrap(value)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"{self.variable}={self.value}*"
