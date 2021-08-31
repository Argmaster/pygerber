# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Tuple

from PIL import Image, ImageDraw
from pygerber.meta.aperture import PolygonAperture
from pygerber.meta.spec import ArcSpec, LineSpec
from pygerber.parser.pillow.apertures.arc_mixin import ArcUtilMixinPillow
from pygerber.parser.pillow.apertures.flash_mixin import FlashUtilMixin


class PillowPolygon(ArcUtilMixinPillow, FlashUtilMixin, PolygonAperture):
    draw_canvas: ImageDraw.ImageDraw

    def draw_shape(self, aperture_stamp_draw: ImageDraw.Draw, color: Tuple):
        pass

    def line(self, spec: LineSpec) -> None:
        self.prepare_line_spec(spec)

    def arc(self, spec: ArcSpec) -> None:
        self.prepare_arc_spec(spec)
