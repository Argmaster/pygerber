"""Macro primitive polygon."""
from __future__ import annotations

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2
from pygerber.gerberx3.parser2.macro2.primitives2.primitive2 import Primitive2


class Code5Polygon2(Primitive2):
    """Polygon macro primitive."""

    # 5 Polygon Exposure, # vertices, Center X, Center Y, Diameter, Rotation 4.5.1.7

    exposure: Expression2
    number_of_vertices: Expression2
    center_x: Expression2
    center_y: Expression2
    diameter: Expression2
    rotation: Expression2
