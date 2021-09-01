# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Tuple
from pygerber.parser.pillow.apertures.flash_line_mixin import FlashLineMixin
from pygerber.parser.pillow.apertures.flash_mixin import FlashUtilMixin
from pygerber.parser.pillow.apertures.arc_mixin import ArcUtilMixinPillow

from PIL import Image, ImageDraw
from pygerber.meta.aperture import CustomAperture


class PillowCustom(ArcUtilMixinPillow, FlashUtilMixin, FlashLineMixin, CustomAperture):
    draw_canvas: ImageDraw.ImageDraw

    # def draw_shape(self, aperture_stamp_draw: ImageDraw.Draw, color: Tuple):
    #     pass
