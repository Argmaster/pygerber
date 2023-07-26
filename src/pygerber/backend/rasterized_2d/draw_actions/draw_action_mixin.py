"""Base class for creating rasterized line draw actions."""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.backend.abstract.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity

if TYPE_CHECKING:
    from pygerber.backend.rasterized_2d.aperture_handle import (
        Rasterized2DPrivateApertureHandle,
    )
    from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend


class Rasterized2DDrawActionMixin:
    """Base class for creating rasterized line drawing actions."""

    # ----------------------------------------------------------------------------------
    # Class which includes this mixin in its inheritance tree must provide following:
    backend: Rasterized2DBackend
    private_handle: Rasterized2DPrivateApertureHandle
    polarity: Polarity

    get_bounding_box: Callable[[], BoundingBox]
    # ----------------------------------------------------------------------------------

    def _draw_aperture(self, position: Vector2D) -> None:
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

    def _draw_bounding_box_if_requested(self) -> None:
        if not self.backend.options.include_bounding_boxes:
            return
        self.draw_bounding_box(
            self.get_bounding_box(),
            self.backend,
            Polarity.DEBUG2,
            1,
        )

    @staticmethod
    def draw_bounding_box(
        box: BoundingBox,
        backend: Rasterized2DBackend,
        polarity: Polarity,
        outline_padding: int,
    ) -> None:
        """Draw bounding box on image target."""
        pixel_box = (box - backend.image_coordinates_correction).as_pixel_box(
            backend.dpi,
            dx_max=+outline_padding,
            dy_max=+outline_padding,
            dx_min=-outline_padding,
            dy_min=-outline_padding,
        )
        backend.image_draw.rectangle(
            xy=pixel_box,
            fill=None,
            outline=polarity.get_2d_rasterized_color(),
            width=1,
        )