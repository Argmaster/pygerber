"""Base class for creating rasterized line draw actions."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pygerber.backend.abstract.draw_actions.draw_line import DrawLine
from pygerber.backend.abstract.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity

if TYPE_CHECKING:
    from pygerber.backend.rasterized_2d.aperture_handle import (
        Rasterized2DPrivateApertureHandle,
    )
    from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend


class Rasterized2DDrawLine(DrawLine):
    """Base class for creating rasterized line drawing actions."""

    backend: Rasterized2DBackend
    private_handle: Rasterized2DPrivateApertureHandle

    def draw(self) -> None:
        """Execute draw action."""
        logging.debug(
            "Drawing line from %s to %s with %s",
            self.start_position,
            self.end_position,
            self.private_handle,
        )
        if not self.private_handle.is_plain_circle:
            logging.warning(
                "Drawing line with aperture %s is invalid. Only plain circular "
                "apertures are allowed.",
                self.private_handle.aperture_id,
            )

        self._draw_line_vertex(self.start_position)

        start = (
            self.start_position - self.backend.image_coordinates_correction
        ).as_pixels(
            self.backend.dpi,
        )
        end = (self.end_position - self.backend.image_coordinates_correction).as_pixels(
            self.backend.dpi,
        )

        aperture_size = self.private_handle.image.size
        width = round((aperture_size[0] + aperture_size[1]) / 2)
        self.backend.image_draw.line(
            (start, end),
            fill=self.polarity.get_1_color(),
            width=width,
        )
        self._draw_line_vertex(self.end_position)

    def _draw_line_vertex(self, position: Vector2D) -> None:
        box = self.private_handle.get_bounding_box()
        image_space_box = box + position - self.backend.image_coordinates_correction
        pixel_box = image_space_box.get_min_vector().as_pixels(self.backend.dpi)

        if self.polarity == Polarity.Dark:
            im = self.private_handle.image
        else:
            im = self.private_handle.image_invert

        self.backend.image.paste(
            im=im,
            box=pixel_box,
            mask=self.private_handle.image,
        )
