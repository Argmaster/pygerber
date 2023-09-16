"""Base class for creating components for aperture creation."""
from __future__ import annotations

import logging
import math
import operator
from decimal import Decimal
from functools import cached_property
from typing import Generator

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.backend.abstract.errors import NoMatchingArcCanterCandidateError
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity

RIGHT_ANGLE_DEGREES = Decimal("95.0")
VERY_SMALL_OFFSET = Offset.new("0.001")


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
        arc_center = self.start_position + self.dx_dy_center

        if self.is_multi_quadrant:
            return arc_center

        for op_x, op_y in (
            (
                operator.pos,
                operator.pos,
            ),
            (
                operator.neg,
                operator.pos,
            ),
            (
                operator.pos,
                operator.neg,
            ),
            (
                operator.neg,
                operator.neg,
            ),
        ):
            offset_vector = Vector2D(
                x=op_x(self.dx_dy_center.x),  # type: ignore[operator]
                y=op_y(self.dx_dy_center.y),  # type: ignore[operator]
            )
            arc_center = self.start_position + offset_vector
            start_position_circle_space = self.start_position - arc_center
            end_position_circle_space = self.end_position - arc_center

            if (
                abs(
                    start_position_circle_space.length()
                    - end_position_circle_space.length(),
                )
                > VERY_SMALL_OFFSET
            ):
                continue

            angle_start, angle_end = self._calculate_start_end_angles_clockwise(
                start_position_circle_space,
                end_position_circle_space,
            )
            angle_delta = angle_end - angle_start
            logging.critical(
                f"{angle_max} - {angle_min} = {angle_delta} ({start_position_circle_space} [{start_position_circle_space.length()}], {end_position_circle_space} [{end_position_circle_space.length()}])",
            )

            if angle_delta < RIGHT_ANGLE_DEGREES:
                return arc_center

        raise NoMatchingArcCanterCandidateError

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

    def _calculate_start_end_angles_clockwise(
        self,
        arc_start_point: Vector2D,
        arc_end_point: Vector2D,
    ) -> tuple[float, float]:
        angle_start = arc_start_point.angle_between_clockwise(Vector2D.UNIT_X)
        angle_end = arc_end_point.angle_between_clockwise(Vector2D.UNIT_X)

        if angle_start == angle_end:
            if self.is_multi_quadrant:
                angle_start = 0
                angle_end = 360
            else:
                angle_start = 0
                angle_end = 0

        return angle_start, angle_end

    def calculate_arc_points(self) -> Generator[Vector2D, None, None]:
        """Calculate points on arc."""
        angle_start, angle_end = self._calculate_start_end_angles_clockwise(
            self.arc_space_start_position,
            self.arc_space_end_position,
        )
        if self.is_clockwise:
            angle_start, angle_end = angle_end, angle_start

        angle_step = 1
        angle_current = angle_start

        yield self.arc_center_absolute

        while angle_current < (angle_end + angle_step):
            yield self.arc_center_absolute + Vector2D(
                x=self.arc_radius * math.cos(math.radians(angle_current)),
                y=self.arc_radius * math.sin(math.radians(angle_current)),
            )
            angle_current = (angle_current + angle_step) % 360

        yield self.arc_center_absolute
