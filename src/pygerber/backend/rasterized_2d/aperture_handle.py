"""Aperture Handle class which represents Gerber X3 aperture."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from PIL import Image, ImageDraw

from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
from pygerber.backend.rasterized_2d.errors import ApertureImageNotInitializedError

if TYPE_CHECKING:
    from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend


class Rasterized2DPrivateApertureHandle(PrivateApertureHandle):
    """Base class for creating Gerber X3 apertures."""

    backend: Rasterized2DBackend
    _image: Optional[Image.Image]

    def finalize_aperture_creation(self) -> None:
        """Draw aperture and store result."""
        bbox = self.get_bounding_box()
        size = bbox.size().as_pixels(self.backend.dpi)

        self.image = Image.new(mode="1", size=size)

        for aperture_draw in self.aperture_draws:
            aperture_draw.draw(self)

        self.image.save("image.png")

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

    @property
    def image_draw(self) -> ImageDraw.ImageDraw:
        """Acquire drawing interface."""
        return ImageDraw.Draw(self.image)