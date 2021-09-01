# -*- coding: utf-8 -*-
from __future__ import annotations
from functools import cached_property
from pygerber.parser.pillow.apertures.flash_line_mixin import FlashLineMixin

from typing import Tuple

from PIL import ImageDraw
from pygerber.meta.aperture import PolygonAperture
from pygerber.meta.spec import ArcSpec, LineSpec
from pygerber.parser.pillow.apertures.arc_mixin import ArcUtilMixinPillow
from pygerber.parser.pillow.apertures.flash_mixin import FlashUtilMixin


class PillowPolygon(
    ArcUtilMixinPillow, FlashUtilMixin, FlashLineMixin, PolygonAperture
):
    draw_canvas: ImageDraw.ImageDraw

    @cached_property
    def radius(self) -> float:
        return int(self._prepare_co(self.DIAMETER) / 2)

    def draw_shape(self, aperture_stamp_draw: ImageDraw.ImageDraw, color: Tuple):
        aperture_stamp_draw.regular_polygon(
            (self.radius, self.radius, self.radius),
            self.VERTICES,
            self.ROTATION - 90,
            color,
            None,
        )

    def arc(self, spec: ArcSpec) -> None:
        self.prepare_arc_spec(spec)
        self.__arc(spec)
        self.flash_at_location(spec.begin)
        self.flash_at_location(spec.end)

    def __arc(self, spec: ArcSpec) -> None:
        for point in self.get_arc_points(spec):
            self.flash_at_location(point.floor())
