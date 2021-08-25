# -*- coding: utf-8 -*-
from __future__ import annotations
from functools import cached_property
from typing import Tuple
from pygerber.mathclasses import Vector2D

from PIL import Image, ImageDraw
from pygerber.meta.aperture import RectangularAperture
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec
from pygerber.parser.pillow.apertures.util import PillowUtilMethdos


class PillowRectangle(RectangularAperture, PillowUtilMethdos):
    draw_canvas: ImageDraw.ImageDraw

    @cached_property
    def x(self) -> float:
        return int(self._prepare_co(self.Y) / 2)

    @cached_property
    def y(self) -> float:
        return int(self._prepare_co(self.X))

    def flash(self, spec: FlashSpec) -> None:
        self.prepare_flash_spec(spec)

    def line(self, spec: LineSpec) -> None:
        self.prepare_line_spec(spec)
        self._flash(spec.location)

    def _flash(self, location: Vector2D) -> None:
        self.draw_canvas.rectangle(self._get_rectangle_bbox(location), self.get_color())

    def _get_ellipse_bbox(self, loc: Vector2D) -> Tuple:
        return (loc.x - self.x, loc.y - self.y, loc.x + self.x, loc.y + self.y)

    def arc(self, spec: ArcSpec) -> None:
        self.prepare_arc_spec(spec)
