"""Macro expression base class, a part which can be used to build more complicated
expressions.

Example of macro expression would be a variable reference, a constant or addition,
everything what can be composed into more complicated structures, but doesn't appear
alone as a macro content. Expressions can be reduced to numerical value during macro
evaluation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.parser2.macro2.element2 import Element2

if TYPE_CHECKING:
    from decimal import Decimal

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Expression2(Element2):
    """Macro expression base class, a part which can be used to build more complicated
    expressions.

    Example of macro expression would be a variable reference, a constant or addition,
    everything what can be composed into more complicated structures, but doesn't appear
    alone as a macro content. Expressions can be reduced to numerical value during macro
    evaluation.
    """

    def on_parser2_eval_expression(self, context: Parser2Context) -> Decimal:
        """Reduce expression to numerical value."""
        raise NotImplementedError
