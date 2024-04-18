"""Base class for creating components for aperture creation."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pygerber.backend.abstract.draw_commands.draw_paste import DrawPaste
from pygerber.backend.abstract.drawing_target import DrawingTarget
from pygerber.backend.rasterized_2d.drawing_target import Rasterized2DDrawingTarget
from pygerber.backend.rasterized_2d.image_tools import replace_color
from pygerber.gerberx3.state_enums import Polarity

if TYPE_CHECKING:
    from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend


class Rasterized2DDrawPaste(DrawPaste):
    """Description of aperture component."""

    other: Rasterized2DDrawingTarget
    backend: Rasterized2DBackend

    def draw(self, target: DrawingTarget) -> None:
        """Apply aperture draw component to handle."""
        if not isinstance(target, Rasterized2DDrawingTarget):
            msg = f"Expected Rasterized2DDrawingTarget got {type(target)}"
            raise TypeError(msg)

        box = self.get_bounding_box()
        image_space_box = box - target.coordinate_origin
        pixel_box = image_space_box.get_min_vector().as_pixels(self.backend.dpi)

        if self.polarity == Polarity.Dark:
            im = self.other.image_polarity_dark

        elif self.polarity == Polarity.Clear:
            im = self.other.image_polarity_clear

        elif self.polarity == Polarity.DarkRegion:
            im = self.other.image_polarity_region_dark

        elif self.polarity == Polarity.ClearRegion:
            im = self.other.image_polarity_region_clear

        else:
            im = replace_color(
                self.other.target_image,
                Polarity.Dark.get_2d_rasterized_color(),
                self.polarity.get_2d_rasterized_color(),
                output_image_mode="L",
            )

        target.target_image.paste(
            im=im,
            box=pixel_box,
            mask=self.other.mask_image,
        )
        logging.debug("Adding %s to %s", self.__class__.__qualname__, target)
