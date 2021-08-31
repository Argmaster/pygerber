# -*- coding: utf-8 -*-
from __future__ import annotations

from functools import cached_property
from pygerber.parser.pillow.apertures.rectangle import PillowRectangle
from typing import Tuple

from PIL import ImageDraw
from pygerber.meta.spec import ArcSpec, LineSpec


class PillowObround(PillowRectangle):
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


