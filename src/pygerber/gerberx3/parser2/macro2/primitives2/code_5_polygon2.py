"""Macro primitive polygon."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2
from pygerber.gerberx3.parser2.macro2.primitives2.primitive2 import Primitive2

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Code5Polygon2(Primitive2):
    """Polygon macro primitive."""

    # 5 Polygon Exposure, # vertices, Center X, Center Y, Diameter, Rotation 4.5.1.7

    exposure: Expression2
    number_of_vertices: Expression2
    center_x: Expression2
    center_y: Expression2
    diameter: Expression2
    rotation: Expression2

    def on_parser2_eval_statement(self, context: Parser2Context) -> None:
        """Evaluate macro to create concrete macro aperture."""
        context.hooks.macro_eval.on_code_5_polygon(context, self)
