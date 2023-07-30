"""Aperture Handle class which represents Gerber X3 aperture."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image

from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
from pygerber.backend.abstract.drawing_target import DrawingTarget
from pygerber.backend.rasterized_2d.drawing_target import Rasterized2DDrawingTarget

if TYPE_CHECKING:
    from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend


class Rasterized2DPrivateApertureHandle(PrivateApertureHandle):
    """Base class for creating Gerber X3 apertures."""

    backend: Rasterized2DBackend
    drawing_target: Rasterized2DDrawingTarget

    def _create_drawing_target(self) -> DrawingTarget:
        """Draw aperture and store result."""
        bbox = self.bounding_box
        size = bbox.get_size().as_pixels(self.backend.dpi)

        # Image must be at least 1x1, otherwise Pillow crashes while saving.
        x, y = size
        size = (max(x, 0) + 1, max(y, 0) + 1)

        return Rasterized2DDrawingTarget(
            coordinate_origin=self.coordinate_origin,
            bounding_box=self.bounding_box,
            target_image=Image.new(mode="L", size=size, color=0),
        )

    def _post_drawing_hook(self) -> None:
        dest = self.backend.options.dump_apertures
        if dest is not None:
            self.drawing_target.target_image.save(
                dest / f"{self.aperture_id}_{self.private_id}.png",
            )
            self.drawing_target.image_invert.save(
                dest / f"{self.aperture_id}_{self.private_id}_I.png",
            )
