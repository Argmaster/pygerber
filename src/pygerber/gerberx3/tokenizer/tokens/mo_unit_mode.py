"""Wrapper for set unit mode token."""
from __future__ import annotations

from enum import Enum

from pygerber.gerberx3.tokenizer.tokens.token import Token


class UnitMode(Token):
    """Wrapper for set unit mode token.

    Sets the unit to mm or inch.
    """

    def __init__(self, unit: str) -> None:
        """Initialize token object."""
        super().__init__()
        self.unit = Unit(unit)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"%MM{self.unit.value}*%"


class Unit(Enum):
    """Aperture unit."""

    Millimeters = "MM"
    Inches = "IN"
