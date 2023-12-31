"""Parser level abstraction of rectangle aperture info for Gerber AST parser,
version 2.
"""

from __future__ import annotations

from typing import Optional

from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2


class Rectangle2(Aperture2):
    """Parser level abstraction of aperture info for rectangle aperture."""

    x_size: Offset
    y_size: Offset
    hole_diameter: Optional[Offset]

    def get_bounding_box_size(self) -> BoundingBox:
        """Return bounding box of aperture."""
        return BoundingBox.from_rectangle(self.x_size, self.y_size)
