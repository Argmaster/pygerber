"""Macro primitive vector line."""
from __future__ import annotations

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2
from pygerber.gerberx3.parser2.macro2.primitives2.primitive2 import Primitive2


class Code20VectorLine2(Primitive2):
    """Vector line macro primitive."""

    exposure: Expression2
    width: Expression2
    start_x: Expression2
    start_y: Expression2
    end_x: Expression2
    end_y: Expression2
    rotation: Expression2
