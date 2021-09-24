# -*- coding: utf-8 -*-
from __future__ import annotations

from PIL import ImageDraw
from pygerber.parser.pillow.apertures.arc_mixin import ArcUtilMixinPillow
from pygerber.parser.pillow.apertures.flash_line_mixin import FlashLineMixin
from pygerber.parser.pillow.apertures.flash_mixin import FlashUtilMixin
from pygerber.renderer.aperture import CustomAperture


class PillowCustom(ArcUtilMixinPillow, FlashUtilMixin, FlashLineMixin, CustomAperture):
    draw_canvas: ImageDraw.ImageDraw

    # def draw_shape(self, aperture_stamp_draw: ImageDraw.Draw, color: Tuple):
    #     pass
