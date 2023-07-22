"""Circle component for creating apertures."""
from __future__ import annotations

from pygerber.backend.abstract.aperture_draws.aperture_draw import ApertureDraw
from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.backend.abstract.offset import Offset
from pygerber.gerberx3.state_enums import Polarity


class ApertureDrawCircle(ApertureDraw):
    """Description of circle aperture component."""

    diameter: Offset
    polarity: Polarity

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        return BoundingBox.from_diameter(self.diameter)
