"""Macro expression base class, a part which can be used to build more complicated
expressions.

Example of macro expression would be a variable reference, a constant or addition,
everything what can be composed into more complicated structures, but doesn't appear
alone as a macro content. Expressions can be reduced to numerical value during macro
evaluation.
"""
from __future__ import annotations

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser2.macro2.element2 import Element2


class Expression2(Element2):
    """Macro expression base class, a part which can be used to build more complicated
    expressions.

    Example of macro expression would be a variable reference, a constant or addition,
    everything what can be composed into more complicated structures, but doesn't appear
    alone as a macro content. Expressions can be reduced to numerical value during macro
    evaluation.
    """

    def visit_evaluate(self) -> Offset:
        """Reduce expression to numerical value."""
        raise NotImplementedError
