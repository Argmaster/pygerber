"""Thermal macro primitive."""
from __future__ import annotations

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2
from pygerber.gerberx3.parser2.macro2.primitives2.primitive2 import Primitive2


class Code7Thermal2(Primitive2):
    """Thermal macro primitive."""

    center_x: Expression2
    center_y: Expression2
    outer_diameter: Expression2
    inner_diameter: Expression2
    gap: Expression2
    rotation: Expression2
