"""Base class for creating components for aperture creation."""

from __future__ import annotations

import math
from functools import cached_property
from typing import Generator

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity


class DrawArc(DrawCommand):
    """Description of aperture component."""

    start_position: Vector2D
    dx_dy_center: Vector2D
    end_position: Vector2D
    width: Offset

    is_clockwise: bool
    is_multi_quadrant: bool

    def __init__(  # noqa: PLR0913
        self,
        backend: Backend,
        polarity: Polarity,
        start_position: Vector2D,
        dx_dy_center: Vector2D,
        end_position: Vector2D,
        width: Offset,
        *,
        is_clockwise: bool,
        is_multi_quadrant: bool,
    ) -> None:
        """Initialize draw command."""
        super().__init__(backend, polarity)
        self.start_position = start_position
        self.dx_dy_center = dx_dy_center
        self.end_position = end_position
        self.width = width
        self.is_clockwise = is_clockwise
        self.is_multi_quadrant = is_multi_quadrant

    @property
    def arc_center_absolute(self) -> Vector2D:
        """Return absolute coordinates of arc center point."""
        return self.start_position + self.dx_dy_center

    @property
    def arc_space_arc_center(self) -> Vector2D:
        """Return arc center coordinates relative to arc center."""
        return self.arc_center_absolute - self.arc_center_absolute

    @property
    def arc_space_start_position(self) -> Vector2D:
        """Return arc start coordinates relative to arc center."""
        return self.start_position - self.arc_center_absolute

    @property
    def arc_space_end_position(self) -> Vector2D:
        """Return arc end coordinates relative to arc center."""
        return self.end_position - self.arc_center_absolute

    @property
    def arc_radius(self) -> Offset:
        """Return arc radius."""
        return self.dx_dy_center.length()

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        return self._bounding_box

    @cached_property
    def _bounding_box(self) -> BoundingBox:
        vertex_box = BoundingBox.from_diameter(self.width)
        radius = self.arc_radius
        return (vertex_box + (self.arc_center_absolute + radius)) + (
            vertex_box + (self.arc_center_absolute - radius)
        )

    def _calculate_angles(self) -> tuple[float, float]:
        angle_start = self.arc_space_start_position.angle_between_clockwise(
            Vector2D.UNIT_Y,
        )
        angle_end = self.arc_space_end_position.angle_between_clockwise(Vector2D.UNIT_Y)

        if self.is_multi_quadrant and angle_start == angle_end:
            angle_start = 0
            angle_end = 360

        elif self.is_clockwise:
            angle_start, angle_end = angle_end, angle_start

        return angle_start, angle_end

    def calculate_arc_points(self) -> Generator[Vector2D, None, None]:
        """Calculate points on arc."""
        angle_start, angle_end = self._calculate_angles()

        angle_step = 1
        angle_min = min(angle_start, angle_end)
        angle_max = max(angle_start, angle_end)

        angle_current = angle_min

        yield self.arc_center_absolute

        while angle_current < (angle_max + angle_step):
            yield self.arc_center_absolute + Vector2D(
                x=self.arc_radius * math.cos(math.radians(angle_current)),
                y=self.arc_radius * math.sin(math.radians(angle_current)),
            )
            angle_current += angle_step

        yield self.arc_center_absolute
