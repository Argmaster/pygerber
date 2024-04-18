"""Thermal macro primitive."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2
from pygerber.gerberx3.parser2.macro2.primitives2.primitive2 import Primitive2

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Code7Thermal2(Primitive2):
    """Thermal macro primitive."""

    center_x: Expression2
    center_y: Expression2
    outer_diameter: Expression2
    inner_diameter: Expression2
    gap: Expression2
    rotation: Expression2

    def on_parser2_eval_statement(self, context: Parser2Context) -> None:
        """Evaluate macro to create concrete macro aperture."""
        context.hooks.macro_eval.on_code_7_thermal(context, self)
