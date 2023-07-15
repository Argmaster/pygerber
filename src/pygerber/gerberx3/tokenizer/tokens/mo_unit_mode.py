"""Wrapper for set unit mode token."""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class UnitMode(Token):
    """Wrapper for set unit mode token.

    Sets the unit to mm or inch.
    """

    unit: Unit

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        unit: Unit = Unit(tokens["unit"])
        return cls(unit=unit)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"%MM{self.unit.value}*%"


class Unit(Enum):
    """Aperture unit."""

    Millimeters = "MM"
    Inches = "IN"
