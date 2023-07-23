"""Polygon component for creating apertures."""
from __future__ import annotations

from decimal import Decimal  # noqa: TCH003

from pygerber.backend.abstract.aperture_draws.aperture_draw import ApertureDraw
from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.backend.abstract.offset import Offset
from pygerber.gerberx3.state_enums import Polarity


class ApertureDrawPolygon(ApertureDraw):
    """Description of polygon aperture component."""

    outer_diameter: Offset
    number_of_vertices: int
    rotation: Decimal
    polarity: Polarity

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        return BoundingBox.from_diameter(self.outer_diameter) + self.center_position
