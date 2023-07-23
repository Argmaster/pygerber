"""Polygon component for creating apertures."""
from __future__ import annotations

import logging
from decimal import Decimal
from typing import TYPE_CHECKING

from pygerber.backend.abstract.aperture_draws.aperture_draw_polygon import (
    ApertureDrawPolygon,
)
from pygerber.backend.rasterized_2d.aperture_handle import (
    Rasterized2DPrivateApertureHandle,
)

if TYPE_CHECKING:
    from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle


class Rasterized2DApertureDrawPolygon(ApertureDrawPolygon):
    """Description of polygon aperture component."""

    def draw(self, handle: PrivateApertureHandle) -> None:
        """Apply aperture draw component to handle."""
        if not isinstance(handle, Rasterized2DPrivateApertureHandle):
            msg = f"Expected Rasterized2DPrivateApertureHandle got {type(handle)}"
            raise TypeError(msg)

        box = self.get_bounding_box()
        coordinate_correction = handle.get_bounding_box().get_min_vector()
        image_space_box = box - coordinate_correction
        center = image_space_box.center.as_pixels(handle.backend.dpi)

        handle.image_draw.regular_polygon(
            bounding_circle=(
                *center,
                (self.outer_diameter / 2).as_pixels(handle.backend.dpi),
            ),
            n_sides=self.number_of_vertices,
            rotation=float(-self.rotation + Decimal("-90.0")),
            fill=self.polarity.get_1_color(),
            outline=None,
            width=0,
        )
        logging.debug("Adding %s to %s", self.__class__.__qualname__, handle)
