"""Circle component for creating apertures."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pygerber.backend.abstract.aperture_draws.aperture_draw_circle import (
    ApertureDrawCircle,
)
from pygerber.backend.rasterized_2d.aperture_handle import (
    Rasterized2DPrivateApertureHandle,
)

if TYPE_CHECKING:
    from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle


class Rasterized2DApertureDrawCircle(ApertureDrawCircle):
    """Description of circle aperture component."""

    def draw(self, handle: PrivateApertureHandle) -> None:
        """Apply aperture draw component to handle."""
        if not isinstance(handle, Rasterized2DPrivateApertureHandle):
            msg = f"Expected Rasterized2DPrivateApertureHandle got {type(handle)}"
            raise TypeError(msg)

        box = self.get_bounding_box()
        coordinate_correction = handle.get_bounding_box().get_min_vector()
        image_space_box = box - coordinate_correction
        pixel_box = image_space_box.as_pixel_box(
            handle.backend.dpi,
        )

        handle.image_draw.ellipse(
            xy=pixel_box,
            fill=self.polarity.get_1_color(),
            outline=None,
            width=0,
        )
        logging.debug("Adding %s to %s", self.__class__.__qualname__, handle)
