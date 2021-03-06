# -*- coding: utf-8 -*-
from __future__ import annotations

from functools import cached_property
from typing import Tuple

from PIL import ImageDraw

from pygerber.mathclasses import BoundingBox, Vector2D
from pygerber.parser.pillow.apertures.arc_mixin import ArcUtilMixinPillow
from pygerber.parser.pillow.apertures.flash_mixin import FlashUtilMixin
from pygerber.renderer.aperture import RectangularAperture
from pygerber.renderer.spec import ArcSpec, LineSpec


class PillowRectangle(ArcUtilMixinPillow, FlashUtilMixin, RectangularAperture):
    draw_canvas: ImageDraw.ImageDraw

    @cached_property
    def x_half(self) -> float:
        return int(self._prepare_co(self.X) / 2)

    @cached_property
    def y_half(self) -> float:
        return int(self._prepare_co(self.Y) / 2)

    def draw_shape(self, aperture_stamp_draw: ImageDraw.Draw, color: Tuple):
        aperture_stamp_draw.rectangle(self.get_aperture_bbox(), color)

    def _get_bbox_at_location(self, loc: Vector2D) -> Tuple:
        return (
            loc.x - self.x_half,
            loc.y - self.y_half,
            loc.x + self.x_half,
            loc.y + self.y_half,
        )

    def line(self, spec: LineSpec) -> None:
        self.prepare_line_spec(spec)
        self.flash_at_location(spec.begin)
        self.flash_at_location(spec.end)
        top, bot = self.__get_top_bot_sides(spec.begin, spec.end)
        self.__draw_side(self.__get_top_site_points(top, bot))
        self.__draw_side(self.__get_bot_site_points(top, bot))
        self.__draw_side(self.__get_left_site_points(top, bot))
        self.__draw_side(self.__get_right_site_points(top, bot))

    def __get_top_bot_sides(self, begin: Vector2D, end: Vector2D) -> BoundingBox:
        return BoundingBox(*self._get_bbox_at_location(begin)), BoundingBox(
            *self._get_bbox_at_location(end)
        )

    def __draw_side(self, points: tuple) -> None:
        self.draw_canvas.polygon(points, self.get_color())

    def __get_top_site_points(self, top: BoundingBox, bot: BoundingBox):
        return (
            (top.left, top.upper),
            (top.right, top.upper),
            (bot.right, bot.upper),
            (bot.left, bot.upper),
        )

    def __get_bot_site_points(self, top: BoundingBox, bot: BoundingBox):
        return (
            (top.left, top.lower),
            (top.right, top.lower),
            (bot.right, bot.lower),
            (bot.left, bot.lower),
        )

    def __get_left_site_points(self, top: BoundingBox, bot: BoundingBox):
        return (
            (top.left, top.lower),
            (top.left, top.upper),
            (bot.left, bot.upper),
            (bot.left, bot.lower),
        )

    def __get_right_site_points(self, top: BoundingBox, bot: BoundingBox):
        return (
            (top.right, top.lower),
            (top.right, top.upper),
            (bot.right, bot.upper),
            (bot.right, bot.lower),
        )

    def arc(self, spec: ArcSpec) -> None:
        self.prepare_arc_spec(spec)
        self.__arc(spec)
        self.flash_at_location(spec.begin)
        self.flash_at_location(spec.end)

    def __arc(self, spec: ArcSpec) -> None:
        for point in self.get_arc_points(spec, self.isCCW):
            self.flash_at_location(point.floor())
