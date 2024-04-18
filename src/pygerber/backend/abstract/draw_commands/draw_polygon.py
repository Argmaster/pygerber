"""Polygon component for creating apertures."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity

if TYPE_CHECKING:
    from decimal import Decimal


class DrawPolygon(DrawCommand):
    """Description of polygon aperture component."""

    center_position: Vector2D
    outer_diameter: Offset
    number_of_vertices: int
    rotation: Decimal

    def __init__(
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
        return self._bounding_box

    @cached_property
    def _bounding_box(self) -> BoundingBox:
        return BoundingBox.from_diameter(self.outer_diameter) + self.center_position
