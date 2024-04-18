"""Macro primitive center line."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2
from pygerber.gerberx3.parser2.macro2.primitives2.primitive2 import Primitive2

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Code21CenterLine2(Primitive2):
    """Center line macro primitive."""

    exposure: Expression2
    width: Expression2
    height: Expression2
    center_x: Expression2
    center_y: Expression2
    rotation: Expression2

    def on_parser2_eval_statement(self, context: Parser2Context) -> None:
        """Evaluate macro to create concrete macro aperture."""
        context.hooks.macro_eval.on_code_21_center_line(context, self)
