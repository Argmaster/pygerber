"""Abstract base class for creating flash draw actions."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pygerber.backend.abstract.draw_actions.draw_flash import DrawFlash

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

        box = (
            self.position
            # Move coordinates to +X +Y (I'st quadrant)
            - self.backend.image_coordinates_correction
            # Move coordinates to upper left of aperture image.
            - (self.private_handle.get_bounding_box().get_size() / 2)
        ).as_pixels(
            self.backend.dpi,
        )

        self.backend.image.paste(
            im=self.private_handle.image,
            box=box,
            mask=self.private_handle.image,
        )
