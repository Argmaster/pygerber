"""Circle component for creating apertures."""
from __future__ import annotations

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.backend.abstract.offset import Offset
from pygerber.backend.abstract.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity


class DrawCircle(DrawCommand):
    """Description of circle aperture component."""

    center_position: Vector2D
    diameter: Offset

    def __init__(
        self,
        backend: Backend,
        polarity: Polarity,
        center_position: Vector2D,
        diameter: Offset,
    ) -> None:
        """Initialize draw command."""
        super().__init__(backend, polarity)
        self.center_position = center_position
        self.diameter = diameter

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        return BoundingBox.from_diameter(self.diameter) + self.center_position
