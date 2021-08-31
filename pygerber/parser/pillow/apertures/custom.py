# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.parser.pillow.apertures.flash_mixin import FlashUtilMixin
from pygerber.parser.pillow.apertures.arc_mixin import ArcUtilMixinPillow

from PIL import Image, ImageDraw
from pygerber.meta.aperture import CustomAperture
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec
from pygerber.parser.pillow.apertures.util import PillowUtilMethdos


class PillowCustom(ArcUtilMixinPillow, FlashUtilMixin, CustomAperture):
    draw_canvas: ImageDraw.ImageDraw

    def line(self, spec: LineSpec) -> None:
        self.prepare_line_spec(spec)

    def arc(self, spec: ArcSpec) -> None:
        self.prepare_arc_spec(spec)
