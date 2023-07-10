"""Macro variable use token."""

from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.macro.element import Element
from pygerber.sequence_tools import unwrap


class MacroVariableName(Element):
    """Wrapper for macro variable use."""

    def __init__(self, name: str) -> None:
        """Initialize token object."""
        super().__init__()
        self.name = unwrap(name)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return self.name
