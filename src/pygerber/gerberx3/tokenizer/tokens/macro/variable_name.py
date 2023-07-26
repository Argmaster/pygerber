"""Macro variable use token."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.sequence_tools import unwrap

if TYPE_CHECKING:
    from typing_extensions import Self


class MacroVariableName(Expression):
    """Wrapper for macro variable use."""

    name: str

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        name = unwrap(tokens["macro_variable_name"])
        return cls(name=name)

    def __str__(self) -> str:
        return self.name
