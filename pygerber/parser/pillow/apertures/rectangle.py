# -*- coding: utf-8 -*-
from __future__ import annotations

from functools import cached_property
from pygerber.parser.pillow.apertures.arc_mixin import ArcUtilMixinPillow
from typing import Tuple

from PIL import Image, ImageDraw
from pygerber.mathclasses import BoundingBox, Vector2D
from pygerber.meta.aperture import RectangularAperture
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec
from pygerber.parser.pillow.apertures.util import PillowUtilMethdos


class PillowRectangle(ArcUtilMixinPillow, PillowUtilMethdos, RectangularAperture):
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

    @cached_property
    def hole_diameter(self) -> float:
        return int(self._prepare_co(self.HOLE_DIAMETER))

    @cached_property
    def hole_radius(self) -> float:
        return int(self._prepare_co(self.HOLE_DIAMETER) / 2)

    @cached_property
    def aperture_mask(self) -> Image.Image:
        aperture_mask, aperture_mask_draw = self.get_aperture_canvas()
        aperture_mask_draw.rectangle(
            self._get_aperture_stamp_bbox(), (255, 255, 255, 255)
        )
        if self.hole_diameter:
            aperture_mask_draw.ellipse(
                self.get_aperture_hole_bbox().as_tuple_y_inverse(),
                (0, 0, 0, 0),
            )
        return aperture_mask

    def get_aperture_canvas(self) -> Image.Image:
        canvas = Image.new(
            "RGBA", (self.x + 1, self.y + 1), (0, 0, 0, 0)
        )
        canvas_draw = ImageDraw.Draw(canvas)
        return canvas, canvas_draw

    @cached_property
    def aperture_stamp_dark(self) -> Image.Image:
        aperture_stamp, aperture_stamp_draw = self.get_aperture_canvas()
        aperture_stamp_draw.rectangle(
            self._get_aperture_stamp_bbox(), self.get_dark_color()
        )
        return aperture_stamp

    @cached_property
    def aperture_stamp_clear(self) -> Image.Image:
        aperture_stamp, aperture_stamp_draw = self.get_aperture_canvas()
        aperture_stamp_draw.rectangle(
            self._get_aperture_stamp_bbox(), self.get_clear_color()
        )
        return aperture_stamp

    def _get_aperture_stamp_bbox(self):
        return 0, 0, self.x - 1, self.y - 1

    def _get_aperture_bbox(self, loc: Vector2D) -> Tuple:
        return (loc.x - self.x_half, loc.y - self.y_half, loc.x + self.x_half, loc.y + self.y_half)

    def flash_offset(self):
        return Vector2D(self.x_half, self.y_half)

    def line(self, spec: LineSpec) -> None:
        self.prepare_line_spec(spec)
        self._flash(spec.begin)
        self._flash(spec.end)
        top, bot = self._get_top_bot_sides(spec.begin, spec.end)
        self._draw_side(self._get_top_site_points(top, bot))
        self._draw_side(self._get_bot_site_points(top, bot))
        self._draw_side(self._get_left_site_points(top, bot))
        self._draw_side(self._get_right_site_points(top, bot))

    def _get_top_bot_sides(self, begin: Vector2D, end: Vector2D) -> BoundingBox:
        return BoundingBox(*self._get_aperture_bbox(begin)), BoundingBox(
            *self._get_aperture_bbox(end)
        )

    def _draw_side(self, points: tuple) -> None:
        self.draw_canvas.polygon(points, self.get_color())

    def _get_top_site_points(self, top: BoundingBox, bot: BoundingBox):
        return (
            (top.left, top.upper),
            (top.right, top.upper),
            (bot.right, bot.upper),
            (bot.left, bot.upper),
        )

    def _get_bot_site_points(self, top: BoundingBox, bot: BoundingBox):
        return (
            (top.left, top.lower),
            (top.right, top.lower),
            (bot.right, bot.lower),
            (bot.left, bot.lower),
        )

    def _get_left_site_points(self, top: BoundingBox, bot: BoundingBox):
        return (
            (top.left, top.lower),
            (top.left, top.upper),
            (bot.left, bot.upper),
            (bot.left, bot.lower),
        )

    def _get_right_site_points(self, top: BoundingBox, bot: BoundingBox):
        return (
            (top.right, top.lower),
            (top.right, top.upper),
            (bot.right, bot.upper),
            (bot.right, bot.lower),
        )

    def arc(self, spec: ArcSpec) -> None:
        self.prepare_arc_spec(spec)
        self._arc(spec)
        self._flash(spec.begin)
        self._flash(spec.end)

    def _arc(self, spec: ArcSpec) -> None:
        for point in self.get_arc_points(spec):
            self._flash(point.floor())
