"""Parser level abstraction of circle aperture info for Gerber AST parser, version 2."""
from __future__ import annotations

from typing import Optional

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2


class Circle2(Aperture2):
    """Parser level abstraction of aperture info for circle aperture."""

    diameter: Offset
    hole_diameter: Optional[Offset]


class NoCircle2(Circle2):
    """Dummy aperture representing case when aperture is not needed but has to be
    given to denote width of draw line command.
    """
