"""Region component for creating apertures."""
from __future__ import annotations

from functools import cached_property

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity


class DrawRegion(DrawCommand):
    """Description of Region aperture component."""

    region_boundary_points: list[Vector2D]

    def __init__(
        self,
        backend: Backend,
        polarity: Polarity,
        region_boundary_points: list[Vector2D],
    ) -> None:
        """Initialize draw command."""
        super().__init__(backend, polarity)
        self.region_boundary_points = region_boundary_points

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        return self._bounding_box

    @cached_property
    def _bounding_box(self) -> BoundingBox:
        box = BoundingBox.from_diameter(Offset.new(0.0))
        for point in self.region_boundary_points:
            box = box.include_point(point)

        return box
