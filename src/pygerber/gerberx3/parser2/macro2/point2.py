"""Container for two macro expressions tied together as point in 2D space."""

from __future__ import annotations

from pygerber.gerberx3.parser2.macro2.element2 import Element2
from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2


class Point2(Element2):
    """Pair of two expressions representing a point in 2D space."""

    x: Expression2
    y: Expression2
