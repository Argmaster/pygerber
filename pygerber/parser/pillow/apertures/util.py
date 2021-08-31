# -*- coding: utf-8 -*-
from __future__ import annotations
from PIL import Image, ImageDraw


from pygerber.mathclasses import BoundingBox, Vector2D
from pygerber.meta.broker import DrawingBroker
from pygerber.meta.meta import Polarity
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec

INCH_TO_MM_MULTIPLIER = 0.0393701


class FlashUtil:
    aperture_stamp_clear: Image.Image
    aperture_stamp_dark: Image.Image
    aperture_mask: Image.Image
    canvas: Image.Image
    draw_canvas: ImageDraw.ImageDraw
    hole_diameter: float

    def flash(self, spec: FlashSpec) -> None:
        self.prepare_flash_spec(spec)
        self._flash(spec.location)

    def _flash(self, location: Vector2D) -> None:
        offset_to_center = location - self.flash_offset()
        if self.is_clear():
            self.canvas.paste(
                self.aperture_stamp_clear,
                offset_to_center.as_tuple(),
                self.aperture_mask,
            )
        else:
            self.canvas.paste(
                self.aperture_stamp_dark,
                offset_to_center.as_tuple(),
                self.aperture_mask,
            )

    def get_aperture_hole_bbox(self) -> BoundingBox:
        return BoundingBox(
            0, 0, self.hole_diameter - 1, self.hole_diameter - 1
        ).transform(
            self.flash_offset()
            - Vector2D(
                self.hole_radius,
                self.hole_radius,
            )
        )


class PillowUtilMethdos(FlashUtil):

    broker: DrawingBroker

    @property
    def dpmm(self):
        return self.broker.dpmm

    @property
    def canvas(self):
        return self.broker.canvas

    @property
    def draw_canvas(self):
        return self.broker.draw_canvas

    @property
    def current_point(self):
        return self.broker.current_point

    def get_color(self):
        if self.is_region():
            return self.get_region_color()
        if self.is_clear():
            return self.get_clear_color()
        else:
            return self.get_dark_color()

    def is_region(self):
        return self.broker.is_regionmode

    def is_clear(self):
        return self.broker.polarity == Polarity.CLEAR

    def get_dark_color(self):
        return self.broker.colors.dark

    def get_clear_color(self):
        return self.broker.colors.clear

    def get_region_color(self):
        return self.broker.colors.region

    def prepare_coordinates(self, vector: Vector2D) -> Vector2D:
        return Vector2D(
            int(self._prepare_co(vector.x) + self.broker.left_offset),
            int(self._prepare_co(vector.y) + self.broker.bottom_offset),
        )

    def _prepare_co(self, value: float) -> float:
        return value * self.dpmm

    def prepare_flash_spec(self, spec: FlashSpec) -> FlashSpec:
        spec.location = self.prepare_coordinates(spec.location)
        return spec

    def prepare_line_spec(self, spec: LineSpec) -> LineSpec:
        spec.begin = self.prepare_coordinates(spec.begin)
        spec.end = self.prepare_coordinates(spec.end)
        return spec

    def prepare_arc_spec(self, spec: ArcSpec) -> ArcSpec:
        spec.begin = self.prepare_coordinates(spec.begin)
        spec.end = self.prepare_coordinates(spec.end)
        spec.center = self.prepare_coordinates(spec.center)
        return spec
