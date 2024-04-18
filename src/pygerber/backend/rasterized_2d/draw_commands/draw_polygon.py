"""Polygon component for creating apertures."""

from __future__ import annotations

import logging
from decimal import Decimal
from typing import TYPE_CHECKING

from pygerber.backend.abstract.draw_commands.draw_polygon import (
    DrawPolygon,
)
from pygerber.backend.abstract.drawing_target import DrawingTarget
from pygerber.backend.rasterized_2d.drawing_target import Rasterized2DDrawingTarget

if TYPE_CHECKING:
    from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend


NUMBER_OF_VERTICES_IN_TRIANGLE = 3


class Rasterized2DApertureDrawPolygon(DrawPolygon):
    """Description of polygon aperture component."""

    backend: Rasterized2DBackend

    def draw(self, target: DrawingTarget) -> None:
        """Apply aperture draw component to handle."""
        if not isinstance(target, Rasterized2DDrawingTarget):
            msg = f"Expected Rasterized2DDrawingTarget got {type(target)}"
            raise TypeError(msg)

        box = self.get_bounding_box()
        image_space_box = box - target.coordinate_origin
        center = image_space_box.center.as_pixels(self.backend.dpi)

        bounding_circle = (
            *center,
            (self.outer_diameter / 2).as_pixels(self.backend.dpi),
        )
        rotation = float(-self.rotation + Decimal("-90.0"))

        if self.number_of_vertices < NUMBER_OF_VERTICES_IN_TRIANGLE:
            logging.warning(
                "Drawing invalid polygon, number of vertices < 3 (%s)",
                self.number_of_vertices,
            )
            return

        (_, __, radius) = bounding_circle
        if radius == 0:
            logging.warning(
                "Drawing zero surface polygon. DPI may be too low. %s",
                bounding_circle,
            )
            return

        target.image_draw.regular_polygon(
            bounding_circle=bounding_circle,
            n_sides=self.number_of_vertices,
            rotation=int(rotation),
            fill=self.polarity.get_2d_rasterized_color(),
            outline=None,
            width=0,
        )
        logging.debug("Adding %s to %s", self.__class__.__qualname__, target)
