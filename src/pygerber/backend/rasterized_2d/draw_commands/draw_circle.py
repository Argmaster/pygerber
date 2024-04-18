"""Circle component for creating apertures."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pygerber.backend.abstract.draw_commands.draw_circle import (
    DrawCircle,
)
from pygerber.backend.abstract.drawing_target import DrawingTarget
from pygerber.backend.rasterized_2d.drawing_target import Rasterized2DDrawingTarget

if TYPE_CHECKING:
    from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend


class Rasterized2DApertureDrawCircle(DrawCircle):
    """Description of circle aperture component."""

    backend: Rasterized2DBackend

    def draw(self, target: DrawingTarget) -> None:
        """Apply aperture draw component to handle."""
        if not isinstance(target, Rasterized2DDrawingTarget):
            msg = f"Expected Rasterized2DDrawingTarget got {type(target)}"
            raise TypeError(msg)

        box = self.get_bounding_box()
        image_space_box = box - target.coordinate_origin
        pixel_box = image_space_box.as_pixel_box(
            self.backend.dpi,
            dx_max=-2,
            dy_max=-2,
            dx_min=+1,
            dy_min=+1,
        )
        (min_x, min_y, max_x, max_y) = pixel_box
        if (max_x - min_x <= 0) or (max_y - min_y <= 0):
            logging.warning(
                "Drawing zero surface circle. DPI may be too low. %s",
                pixel_box,
            )

        else:
            target.image_draw.ellipse(
                xy=pixel_box,
                fill=self.polarity.get_2d_rasterized_color(),
                outline=None,
                width=0,
            )
            logging.debug("Adding %s to %s", self.__class__.__qualname__, target)
