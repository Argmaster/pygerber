"""Macro statement base class.

A statement is everything what have to appear alone, for example a primitive or a
variable assignment. Statements by themselves can't be reduced to numerical value during
macro evaluation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.parser2.macro2.element2 import Element2

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Statement2(Element2):
    """Macro statement base class.

    A statement is everything what have to appear alone, for example a primitive or a
    variable assignment. Statements by themselves can't be reduced to numerical value
    during macro evaluation.
    """

    def on_parser2_eval_statement(self, context: Parser2Context) -> None:
        """Evaluate macro to create concrete macro aperture."""
        raise NotImplementedError
