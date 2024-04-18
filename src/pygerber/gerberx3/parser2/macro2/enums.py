"""`enums` module contains Exposure2 enumeration containing possible macro primitive
exposures.
"""

from __future__ import annotations

from enum import Enum


class Exposure(Enum):
    """Macro primitive exposure."""

    ON = 1
    OFF = 0
