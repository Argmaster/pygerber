"""`assignment2` module contains a `Assignment2` class wrapping variable assignment
within macro definition.
"""
from __future__ import annotations

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2
from pygerber.gerberx3.parser2.macro2.statement2 import Statement2


class Assignment2(Statement2):
    """Variable assignment."""

    variable_name: str
    value: Expression2
