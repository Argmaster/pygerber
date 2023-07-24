"""Aperture Handle class which represents Gerber X3 aperture."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from PIL import Image, ImageDraw

from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
from pygerber.backend.rasterized_2d.errors import ApertureImageNotInitializedError

if TYPE_CHECKING:
    from pathlib import Path

    from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend


class Rasterized2DPrivateApertureHandle(PrivateApertureHandle):
    """Base class for creating Gerber X3 apertures."""

    backend: Rasterized2DBackend
    _image: Optional[Image.Image]

    def finalize_aperture_creation(self) -> None:
        """Draw aperture and store result."""
        bbox = self.get_bounding_box()

        size = bbox.get_size().as_pixels(self.backend.dpi)

        # Image must be at least 1x1, otherwise Pillow crashes while saving.
        x, y = size
        size = (max(x, 0) + 1, max(y, 0) + 1)

        self.image = Image.new(mode="L", size=size, color=0)

        for aperture_draw in self.aperture_draws:
            aperture_draw.draw(self)

        self.image = self.image

    @property
    def image(self) -> Image.Image:
        """Aperture image."""
        if self._image is None:
            raise ApertureImageNotInitializedError
        return self._image

    @image.setter
    def image(self, value: Image.Image) -> None:
        """Aperture image."""
        self._image = value
        self._image_invert = self._image.point(lambda p: 1 - p)

    @property
    def image_draw(self) -> ImageDraw.ImageDraw:
        """Acquire drawing interface."""
        return ImageDraw.Draw(self.image)

    @property
    def image_invert(self) -> Image.Image:
        """Inverted aperture image."""
        if self._image_invert is None:
            raise ApertureImageNotInitializedError
        return self._image_invert

    def dump_aperture(self, dest: Path) -> None:
        """Save aperture to local file, mainly for debugging purposes."""
        self.image.save(dest / f"{self.aperture_id}_{self.private_id}.png")
        self.image_invert.save(dest / f"{self.aperture_id}_{self.private_id}_I.png")
