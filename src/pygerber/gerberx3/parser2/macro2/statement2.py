"""Macro statement base class.

A statement is everything what have to appear alone, for example a primitive or a
variable assignment. Statements by themselves can't be reduced to numerical value during
macro evaluation.
"""
from __future__ import annotations

from pygerber.gerberx3.parser2.macro2.element2 import Element2


class Statement2(Element2):
    """Macro statement base class.

    A statement is everything what have to appear alone, for example a primitive or a
    variable assignment. Statements by themselves can't be reduced to numerical value
    during macro evaluation.
    """
