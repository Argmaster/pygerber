"""Class for drawing 2D rasterized vector lines."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pygerber.backend.abstract.draw_commands.draw_region import DrawRegion
from pygerber.backend.abstract.drawing_target import DrawingTarget
from pygerber.backend.rasterized_2d.drawing_target import Rasterized2DDrawingTarget

if TYPE_CHECKING:
    from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend


NUMBER_OF_VERTICES_IN_TRIANGLE = 3


class Rasterized2DDrawRegion(DrawRegion):
    """Draw 2D rasterized vector line."""

    backend: Rasterized2DBackend

    def draw(self, target: DrawingTarget) -> None:
        """Apply aperture draw component to handle."""
        if not isinstance(target, Rasterized2DDrawingTarget):
            msg = f"Expected Rasterized2DDrawingTarget got {type(target)}"
            raise TypeError(msg)

        boundary_points: list[tuple[int, int]] = []

        for point in self.region_boundary_points:
            pixel_point = (point - target.coordinate_origin).as_pixels(
                self.backend.dpi,
            )
            boundary_points.append(pixel_point)

        if len(boundary_points) < NUMBER_OF_VERTICES_IN_TRIANGLE:
            logging.warning(
                "Drawing invalid region, number of vertices < 3 (%s)",
                len(boundary_points),
            )
            return

        target.image_draw.polygon(
            boundary_points,
            fill=self.polarity.get_2d_rasterized_color(),
        )
        logging.debug("Adding %s to %s", self.__class__.__qualname__, target)
