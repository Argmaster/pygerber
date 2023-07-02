"""Coordinate wrapper class."""
from __future__ import annotations

from enum import Enum


class Coordinate:
    """Coordinate wrapper class."""

    def __init__(self, coordinate_type: CoordinateType, raw: str) -> None:
        """Initialize raw coordinate."""
        self.coordinate_type = coordinate_type
        self.raw = raw

    def __str__(self) -> str:
        """Return pretty representation of coordinate token."""
        return f"{self.coordinate_type.value}{self.raw}"


class CoordinateType(Enum):
    """Type of coordinate axis/meaning."""

    X = "X"
    Y = "Y"
    I = "I"  # noqa: E741
    J = "J"
    NULL = ""
