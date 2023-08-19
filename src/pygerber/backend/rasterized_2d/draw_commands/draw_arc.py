"""Class for drawing 2D rasterized vector lines."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pygerber.backend.abstract.draw_commands.draw_arc import DrawArc
from pygerber.backend.abstract.drawing_target import DrawingTarget
from pygerber.backend.rasterized_2d.drawing_target import Rasterized2DDrawingTarget
from pygerber.gerberx3.math.vector_2d import Vector2D

if TYPE_CHECKING:
    from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend


class Rasterized2DDrawArc(DrawArc):
    """Draw 2D rasterized vector line."""

    backend: Rasterized2DBackend

    def draw(self, target: DrawingTarget) -> None:
        """Apply aperture draw component to handle."""
        if not isinstance(target, Rasterized2DDrawingTarget):
            msg = f"Expected Rasterized2DDrawingTarget got {type(target)}"
            raise TypeError(msg)

        bbox = self.get_bounding_box() - target.coordinate_origin
        pixel_box = bbox.as_pixel_box(self.backend.dpi)

        angle_start = self.arc_space_start_position.angle_between_clockwise(
            Vector2D.UNIT_Y,
        )
        angle_end = self.arc_space_end_position.angle_between_clockwise(Vector2D.UNIT_Y)

        if self.is_multi_quadrant and angle_start == angle_end:
            angle_start = 0
            angle_end = 360

        elif self.is_clockwise:
            angle_start, angle_end = angle_end, angle_start

        width = self.width.as_pixels(self.backend.dpi)

        target.image_draw.arc(
            xy=pixel_box,
            start=angle_start,
            end=angle_end,
            fill=self.polarity.get_2d_rasterized_color(),
            width=width,
        )
        logging.debug("Adding %s to %s", self.__class__.__qualname__, target)
