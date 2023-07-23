"""Abstract base class for creating flash draw actions."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pygerber.backend.abstract.draw_actions.draw_flash import DrawFlash
from pygerber.gerberx3.state_enums import Polarity

if TYPE_CHECKING:
    from pygerber.backend.rasterized_2d.aperture_handle import (
        Rasterized2DPrivateApertureHandle,
    )
    from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend


class Rasterized2DDrawFlash(DrawFlash):
    """Class for creating rasterized 2D flashes."""

    backend: Rasterized2DBackend
    private_handle: Rasterized2DPrivateApertureHandle

    def draw(self) -> None:
        """Execute draw action."""
        logging.debug("Flashing at %s with %s", self.position, self.private_handle)

        box = self.get_bounding_box()  # Bounding box includes aperture position.

        image_space_box = box - self.backend.image_coordinates_correction
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
