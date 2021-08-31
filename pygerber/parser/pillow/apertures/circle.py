# -*- coding: utf-8 -*-
from __future__ import annotations

from functools import cached_property
from pygerber.parser.pillow.apertures.arc_mixin import ArcUtilMixinPillow
from typing import Tuple

from PIL import Image, ImageDraw
from pygerber.mathclasses import BoundingBox, Vector2D
from pygerber.meta.aperture import CircularAperture
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec
from pygerber.parser.pillow.apertures.util import PillowUtilMethdos


class PillowCircle(ArcUtilMixinPillow, PillowUtilMethdos, CircularAperture):
    canvas: Image.Image
    draw_canvas: ImageDraw.ImageDraw

    @cached_property
    def radius(self) -> float:
        return int(self._prepare_co(self.DIAMETER) / 2)

    @cached_property
    def diameter(self) -> float:
        return int(self._prepare_co(self.DIAMETER))

    @cached_property
    def hole_diameter(self) -> float:
        return int(self._prepare_co(self.HOLE_DIAMETER))

    @cached_property
    def hole_radius(self) -> float:
        return int(self._prepare_co(self.HOLE_DIAMETER) / 2)

    @cached_property
    def aperture_mask(self) -> Image.Image:
        aperture_mask, aperture_mask_draw = self.get_aperture_canvas()
        aperture_mask_draw.ellipse(self._get_aperture_bbox( ), (255, 255, 255, 255))
        if self.hole_diameter:
            aperture_mask_draw.ellipse(
                self.get_aperture_hole_bbox().as_tuple_y_inverse(),
                (0, 0, 0, 0),
            )
        return aperture_mask

    def get_aperture_canvas(self) -> Image.Image:
        canvas = Image.new(
            "RGBA", (self.diameter + 1, self.diameter + 1), (0, 0, 0, 0)
        )
        canvas_draw = ImageDraw.Draw(canvas)
        return canvas, canvas_draw

    @cached_property
    def aperture_stamp_dark(self) -> Image.Image:
        aperture_stamp, aperture_stamp_draw = self.get_aperture_canvas()
        aperture_stamp_draw.ellipse(self._get_aperture_bbox(), self.get_dark_color())
        return aperture_stamp

    @cached_property
    def aperture_stamp_clear(self) -> Image.Image:
        aperture_stamp, aperture_stamp_draw = self.get_aperture_canvas()
        aperture_stamp_draw.ellipse(self._get_aperture_bbox(), self.get_clear_color())
        return aperture_stamp

    def _get_aperture_bbox(self) -> Tuple[float]:
        return 0, 0, self.diameter - 1, self.diameter - 1

    def flash_offset(self):
        return Vector2D(self.radius, self.radius)

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
