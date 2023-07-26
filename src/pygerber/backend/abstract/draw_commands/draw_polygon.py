"""Polygon component for creating apertures."""
from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.backend.abstract.offset import Offset
from pygerber.backend.abstract.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity

if TYPE_CHECKING:
    from decimal import Decimal


class DrawPolygon(DrawCommand):
    """Description of polygon aperture component."""

    center_position: Vector2D
    outer_diameter: Offset
    number_of_vertices: int
    rotation: Decimal

    def __init__(  # noqa: PLR0913
        self,
        backend: Backend,
        polarity: Polarity,
        center_position: Vector2D,
        outer_diameter: Offset,
        number_of_vertices: int,
        rotation: Decimal,
    ) -> None:
        """Initialize draw command."""
        super().__init__(backend, polarity)
        self.center_position = center_position
        self.outer_diameter = outer_diameter
        self.number_of_vertices = number_of_vertices
        self.rotation = rotation

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        return BoundingBox.from_diameter(self.outer_diameter) + self.center_position
