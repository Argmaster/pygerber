"""Coordinate wrapper class."""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class Coordinate(BaseModel):
    """Coordinate wrapper class."""

    coordinate_type: CoordinateType
    raw_offset: str

    def __str__(self) -> str:
        """Return pretty representation of coordinate token."""
        return f"{self.coordinate_type.value}{self.raw_offset}"


class CoordinateType(Enum):
    """Type of coordinate axis/meaning."""

    X = "X"
    Y = "Y"
    I = "I"  # noqa: E741
    J = "J"
    NULL = ""
