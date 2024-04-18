"""Class for drawing 2D rasterized vector lines."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pygerber.backend.abstract.draw_commands.draw_vector_line import DrawVectorLine
from pygerber.backend.abstract.drawing_target import DrawingTarget
from pygerber.backend.rasterized_2d.drawing_target import Rasterized2DDrawingTarget

if TYPE_CHECKING:
    from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend


class Rasterized2DDrawVectorLine(DrawVectorLine):
    """Draw 2D rasterized vector line."""

    backend: Rasterized2DBackend

    def draw(self, target: DrawingTarget) -> None:
        """Apply aperture draw component to handle."""
        if not isinstance(target, Rasterized2DDrawingTarget):
            msg = f"Expected Rasterized2DDrawingTarget got {type(target)}"
            raise TypeError(msg)

        start = (self.start_position - target.coordinate_origin).as_pixels(
            self.backend.dpi,
        )
        end = (self.end_position - target.coordinate_origin).as_pixels(
            self.backend.dpi,
        )
        width = self.width.as_pixels(self.backend.dpi)

        target.image_draw.line(
            (start, end),
            fill=self.polarity.get_2d_rasterized_color(),
            width=width,
        )
        logging.debug("Adding %s to %s", self.__class__.__qualname__, target)
