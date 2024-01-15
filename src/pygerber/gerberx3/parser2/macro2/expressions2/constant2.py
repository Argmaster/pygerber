"""`constant2` module contain class wrapping constant value in macro definition."""
from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Constant2(Expression2):
    """Class wrapping constant value in macro definition."""

    value: Offset

    def on_parser2_eval_expression(
        self,
        context: Parser2Context,  # noqa: ARG002
    ) -> Offset:
        """Reduce expression to numerical value."""
        return self.value
