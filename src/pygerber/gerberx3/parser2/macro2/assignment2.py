"""`assignment2` module contains a `Assignment2` class wrapping variable assignment
within macro definition.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2
from pygerber.gerberx3.parser2.macro2.statement2 import Statement2

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Assignment2(Statement2):
    """Variable assignment."""

    variable_name: str
    value: Expression2

    def on_parser2_eval_statement(self, context: Parser2Context) -> None:
        """Evaluate macro to create concrete macro aperture."""
        context.hooks.macro_eval.on_assignment(context, self)
