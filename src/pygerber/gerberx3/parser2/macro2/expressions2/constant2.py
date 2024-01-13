"""`constant2` module contain class wrapping constant value in macro definition."""
from __future__ import annotations

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2


class Constant2(Expression2):
    """Class wrapping constant value in macro definition."""

    value: Offset
