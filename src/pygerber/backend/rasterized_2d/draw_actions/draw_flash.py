"""Abstract base class for creating flash draw actions."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pygerber.backend.abstract.draw_actions.draw_flash import DrawFlash
from pygerber.backend.rasterized_2d.draw_actions.draw_action_mixin import (
    Rasterized2DDrawActionMixin,
)

if TYPE_CHECKING:
    from pygerber.backend.rasterized_2d.aperture_handle import (
        Rasterized2DPrivateApertureHandle,
    )
    from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend


class Rasterized2DDrawFlash(DrawFlash, Rasterized2DDrawActionMixin):
    """Class for creating rasterized 2D flashes."""

    backend: Rasterized2DBackend
    private_handle: Rasterized2DPrivateApertureHandle

    def draw(self) -> None:
        """Execute draw action."""
        logging.debug("Flashing at %s with %s", self.position, self.private_handle)

        self._draw_aperture(self.position)
        self._draw_bounding_box_if_requested()
