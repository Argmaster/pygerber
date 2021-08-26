# -*- coding: utf-8 -*-
from __future__ import annotations
from functools import cached_property
from typing import Tuple
from pygerber.mathclasses import BoundingBox, Vector2D

from PIL import Image, ImageDraw
from pygerber.meta.aperture import RectangularAperture
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec
from pygerber.parser.pillow.apertures.util import PillowFlashArcMixin, PillowUtilMethdos


class PillowRectangle(RectangularAperture, PillowUtilMethdos, PillowFlashArcMixin):
    draw_canvas: ImageDraw.ImageDraw

    @cached_property
    def x(self) -> float:
        return int(self._prepare_co(self.Y))

    @cached_property
    def y(self) -> float:
        return int(self._prepare_co(self.X))

    def flash(self, spec: FlashSpec) -> None:
        self.prepare_flash_spec(spec)
        self._flash(spec.location)

    def _flash(self, location: Vector2D) -> None:
        self.draw_canvas.rectangle(self._get_rectangle_bbox(location), self.get_color())

    def _get_rectangle_bbox(self, loc: Vector2D) -> Tuple:
        return (loc.x - self.x, loc.y - self.y, loc.x + self.x, loc.y + self.y)

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
        return BoundingBox(*self._get_rectangle_bbox(begin)), BoundingBox(
            *self._get_rectangle_bbox(end)
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
        begin_angle, end_angle = self._get_begin_end_angles(spec)
        if begin_angle > end_angle:
            begin_angle -= 360
        self._arc_of_flashes(spec, begin_angle, end_angle)
