# -*- coding: utf-8 -*-
from __future__ import annotations

from functools import cached_property
from typing import Tuple

from PIL import Image, ImageDraw
from pygerber.meta.aperture import RectangularAperture
from pygerber.meta.spec import ArcSpec, LineSpec
from pygerber.parser.pillow.apertures.arc_mixin import ArcUtilMixinPillow
from pygerber.parser.pillow.apertures.flash_mixin import FlashUtilMixin


class PillowObround(ArcUtilMixinPillow, FlashUtilMixin, RectangularAperture):
    draw_canvas: ImageDraw.ImageDraw

    @cached_property
    def x(self) -> float:
        return int(self._prepare_co(self.X))

    @cached_property
    def x_half(self) -> float:
        return int(self._prepare_co(self.X) / 2)

    @cached_property
    def y(self) -> float:
        return int(self._prepare_co(self.Y))

    @cached_property
    def y_half(self) -> float:
        return int(self._prepare_co(self.Y) / 2)

    def draw_shape(self, aperture_stamp_draw: ImageDraw.Draw, color: Tuple):
        aperture_stamp_draw.rounded_rectangle(
            self.get_aperture_bbox(),
            min(self.x_half, self.y_half),
            color,
        )

    def line(self, spec: LineSpec) -> None:
        self.prepare_line_spec(spec)

    def arc(self, spec: ArcSpec) -> None:
        self.prepare_arc_spec(spec)
