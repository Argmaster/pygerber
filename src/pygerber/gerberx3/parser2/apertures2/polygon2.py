"""Parser level abstraction of polygon aperture info for Gerber AST parser,
version 2.
"""
from __future__ import annotations

from decimal import Decimal  # noqa: TCH003
from typing import Optional

from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2


class Polygon2(Aperture2):
    """Parser level abstraction of aperture info for polygon aperture."""

    outer_diameter: Offset
    number_vertices: int
    rotation: Decimal
    hole_diameter: Optional[Offset]

    def get_bounding_box_size(self) -> BoundingBox:
        """Return bounding box of aperture."""
        return BoundingBox.from_diameter(self.outer_diameter)
