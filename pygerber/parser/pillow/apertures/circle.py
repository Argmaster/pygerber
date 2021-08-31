# -*- coding: utf-8 -*-
from __future__ import annotations

from functools import cached_property
from typing import Tuple
from pygerber.parser.pillow.apertures.flash_mixin import FlashUtilMixin
from pygerber.parser.pillow.apertures.arc_mixin import ArcUtilMixinPillow

from PIL import Image, ImageDraw
from pygerber.mathclasses import Vector2D
from pygerber.meta.aperture import CircularAperture
from pygerber.meta.spec import ArcSpec, LineSpec


class PillowCircle(ArcUtilMixinPillow, FlashUtilMixin, CircularAperture):
    canvas: Image.Image
    draw_canvas: ImageDraw.ImageDraw

    @cached_property
    def radius(self) -> float:
        return int(self._prepare_co(self.DIAMETER) / 2)

    @cached_property
    def diameter(self) -> float:
        return int(self._prepare_co(self.DIAMETER))

    def draw_shape(self, aperture_stamp_draw: ImageDraw.Draw, color: Tuple):
        aperture_stamp_draw.ellipse(self.get_aperture_bbox(), color)

    def line(self, spec: LineSpec) -> None:
        self.prepare_line_spec(spec)
        self._line(spec.begin, spec.end)
        self._flash(spec.begin)
        self._flash(spec.end)

    def _line(self, begin: Vector2D, end: Vector2D) -> None:
        self.draw_canvas.line(
            [begin.as_tuple(), end.as_tuple()],
            self.get_color(),
            width=self.diameter,
        )

    def arc(self, spec: ArcSpec) -> None:
        self.prepare_arc_spec(spec)
        self._arc(spec)
        self._flash(spec.begin)
        self._flash(spec.end)

    def _arc(self, spec: ArcSpec):
        begin_angle, end_angle = self.get_begin_end_angles(spec)
        if self.isCCW:
            self._draw_arc(spec, begin_angle, end_angle)
        else:
            self._draw_arc(spec, -begin_angle, -end_angle)

    def _draw_arc(self, spec, begin_angle, end_angle):
        self.draw_canvas.arc(
            self._get_arc_bbox(spec),
            begin_angle,
            end_angle,
            self.get_color(),
            width=self.diameter,
        )

    def _get_arc_bbox(self, spec: ArcSpec) -> tuple:
        radius = (spec.begin - spec.center).length() + self.radius
        return (
            spec.center.x - radius,
            spec.center.y - radius,
            spec.center.x + radius,
            spec.center.y + radius,
        )
