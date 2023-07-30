"""Target for Draw commands to draw into."""
from __future__ import annotations

from typing import Optional

from PIL import Image, ImageDraw

from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.backend.abstract.drawing_target import DrawingTarget
from pygerber.backend.abstract.vector_2d import Vector2D
from pygerber.backend.rasterized_2d.errors import ApertureImageNotInitializedError


class Rasterized2DDrawingTarget(DrawingTarget):
    """Target for Draw commands to draw into."""

    target_image: Image.Image
    target_invert_invert: Optional[Image.Image] = None

    def __init__(
        self,
        coordinate_origin: Vector2D,
        bounding_box: BoundingBox,
        target_image: Image.Image,
        target_invert_invert: Optional[Image.Image] = None,
    ) -> None:
        """Initialize drawing target."""
        super().__init__(coordinate_origin, bounding_box)
        self.target_image = target_image
        self.target_invert_invert = target_invert_invert

    @property
    def image_draw(self) -> ImageDraw.ImageDraw:
        """Acquire drawing interface."""
        return ImageDraw.Draw(self.target_image)

    def _finalize(self) -> None:
        self.target_invert_invert = self.target_image.point(lambda p: 1 - p)

    @property
    def image_invert(self) -> Image.Image:
        """Inverted aperture image."""
        if self.target_invert_invert is None:
            raise ApertureImageNotInitializedError

        return self.target_invert_invert
