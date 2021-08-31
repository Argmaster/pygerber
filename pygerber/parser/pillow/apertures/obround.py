# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.parser.pillow.apertures.arc_mixin import ArcUtilMixinPillow

from PIL import Image, ImageDraw
from pygerber.meta.aperture import RectangularAperture
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec
from pygerber.parser.pillow.apertures.util import PillowUtilMethdos


class PillowObround(ArcUtilMixinPillow, RectangularAperture, PillowUtilMethdos):
    draw_canvas: ImageDraw.ImageDraw

    def flash(self, spec: FlashSpec) -> None:
        self.prepare_flash_spec(spec)

    def line(self, spec: LineSpec) -> None:
        self.prepare_line_spec(spec)

    def arc(self, spec: ArcSpec) -> None:
        self.prepare_arc_spec(spec)
