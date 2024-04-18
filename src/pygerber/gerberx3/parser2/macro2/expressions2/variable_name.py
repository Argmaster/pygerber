"""Module `variable_name.py` contains a class `VariableName` used to wrap variable
name.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2

if TYPE_CHECKING:
    from decimal import Decimal

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class VariableName2(Expression2):
    """Class wrapping variable name in macro definition."""

    name: str

    def on_parser2_eval_expression(self, context: Parser2Context) -> Decimal:
        """Reduce expression to numerical value."""
        return context.macro_variable_buffer[self.name]
