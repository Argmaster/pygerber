"""Rectangle component for creating apertures."""
from __future__ import annotations

from pygerber.backend.abstract.aperture_draws.aperture_draw import ApertureDraw
from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.backend.abstract.offset import Offset
from pygerber.gerberx3.state_enums import Polarity


class ApertureDrawRectangle(ApertureDraw):
    """Description of rectangle aperture component."""

    x_size: Offset
    y_size: Offset
    polarity: Polarity

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        return (
            BoundingBox.from_rectangle(self.x_size, self.y_size) + self.center_position
        )
