"""Target for Draw commands to draw into."""

from __future__ import annotations

from typing import Optional

from PIL import Image, ImageDraw

from pygerber.backend.abstract.drawing_target import DrawingTarget
from pygerber.backend.rasterized_2d.errors import ApertureImageNotInitializedError
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity

GRAYSCALE_CENTER_VALUE: int = 127


class Rasterized2DDrawingTarget(DrawingTarget):
    """Target for Draw commands to draw into."""

    target_image: Image.Image
    _target_image_polarity_dark: Optional[Image.Image] = None
    _target_image_polarity_clear: Optional[Image.Image] = None
    _target_image_polarity_region_dark: Optional[Image.Image] = None
    _target_image_polarity_region_clear: Optional[Image.Image] = None
    _mask_image: Optional[Image.Image] = None

    def __init__(
        self,
        coordinate_origin: Vector2D,
        bounding_box: BoundingBox,
        target_image: Image.Image,
    ) -> None:
        """Initialize drawing target."""
        super().__init__(coordinate_origin, bounding_box)
        self.target_image = target_image
        self._target_image_polarity_dark = None
        self._target_image_polarity_clear = None
        self._target_image_polarity_region_dark = None
        self._target_image_polarity_region_clear = None
        self._mask_image = None
        self._is_finalized = False

    @property
    def image_draw(self) -> ImageDraw.ImageDraw:
        """Acquire drawing interface."""
        return ImageDraw.Draw(self.target_image)

    def _finalize(self) -> None:
        self._is_finalized = True

    @property
    def mask_image(self) -> Image.Image:
        """Inverted aperture image."""
        if not self._is_finalized:
            raise ApertureImageNotInitializedError

        if self._mask_image is None:
            self._mask_image = self.target_image.point(
                lambda p: 255 if p > GRAYSCALE_CENTER_VALUE else 0,
            )

        return self._mask_image

    @property
    def image_polarity_dark(self) -> Image.Image:
        """Inverted aperture image."""
        if not self._is_finalized:
            raise ApertureImageNotInitializedError

        if self._target_image_polarity_dark is None:
            color = Polarity.Dark.get_2d_rasterized_color()
            self._target_image_polarity_dark = self.mask_image.point(
                lambda p: color if p else 0,
            )

        return self._target_image_polarity_dark

    @property
    def image_polarity_clear(self) -> Image.Image:
        """Inverted aperture image."""
        if not self._is_finalized:
            raise ApertureImageNotInitializedError

        if self._target_image_polarity_clear is None:
            color = Polarity.Clear.get_2d_rasterized_color()
            self._target_image_polarity_clear = self.mask_image.point(
                lambda p: color if p else 0,
            )

        return self._target_image_polarity_clear

    @property
    def image_polarity_region_dark(self) -> Image.Image:
        """Inverted aperture image."""
        if not self._is_finalized:
            raise ApertureImageNotInitializedError

        if self._target_image_polarity_region_dark is None:
            color = Polarity.DarkRegion.get_2d_rasterized_color()
            self._target_image_polarity_region_dark = self.mask_image.point(
                lambda p: color if p else 0,
            )

        return self._target_image_polarity_region_dark

    @property
    def image_polarity_region_clear(self) -> Image.Image:
        """Inverted aperture image."""
        if not self._is_finalized:
            raise ApertureImageNotInitializedError

        if self._target_image_polarity_region_clear is None:
            color = Polarity.ClearRegion.get_2d_rasterized_color()
            self._target_image_polarity_region_clear = self.mask_image.point(
                lambda p: color if p else 0,
            )

        return self._target_image_polarity_region_clear
