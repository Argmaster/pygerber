# -*- coding: utf-8 -*-
from __future__ import annotations

from pygerber.parser.pillow.apertures.flash_line_mixin import FlashLineMixin
from pygerber.parser.pillow.apertures.rectangle import PillowRectangle
from typing import Tuple

from PIL import ImageDraw


class PillowObround(FlashLineMixin, PillowRectangle):
    draw_canvas: ImageDraw.ImageDraw

    def draw_shape(self, aperture_stamp_draw: ImageDraw.Draw, color: Tuple):
        aperture_stamp_draw.rounded_rectangle(
            self.get_aperture_bbox(),
            min(self.x_half, self.y_half),
            color,
        )
