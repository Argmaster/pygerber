"""Macro primitive circle."""
from __future__ import annotations

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2
from pygerber.gerberx3.parser2.macro2.primitives2.primitive2 import Primitive2


class Code1Circle2(Primitive2):
    """Circle macro primitive."""

    exposure: Expression2
    diameter: Expression2
    center_x: Expression2
    center_y: Expression2
    rotation: Expression2
