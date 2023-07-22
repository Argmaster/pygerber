"""Circle component for creating apertures."""
from __future__ import annotations

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

        handle.image_draw.ellipse(
            self.get_bounding_box()
            .reposition_to_zero()
            .as_pixel_box(handle.backend.dpi, max_value_correction=-1),
            fill=self.polarity.get_1_color(),
        )