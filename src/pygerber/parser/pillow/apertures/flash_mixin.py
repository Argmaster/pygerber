# -*- coding: utf-8 -*-
from __future__ import annotations

from functools import cached_property
from typing import Tuple

from PIL import Image, ImageDraw
from pygerber.mathclasses import BoundingBox, Vector2D
from pygerber.parser.pillow.apertures.util import PillowUtilMethdos
from pygerber.renderer.spec import FlashSpec


class FlashUtilMixin(PillowUtilMethdos):
    aperture_stamp_clear: Image.Image
    aperture_stamp_dark: Image.Image
    aperture_mask: Image.Image
    canvas: Image.Image
    draw_canvas: ImageDraw.ImageDraw
    hole_diameter: float
    hole_radius: float

    @cached_property
    def hole_diameter(self) -> float:
        return int(self._prepare_co(self.HOLE_DIAMETER))

    @cached_property
    def hole_radius(self) -> float:
        return int(self._prepare_co(self.HOLE_DIAMETER) / 2)

    @cached_property
    def aperture_mask(self) -> Image.Image:
        aperture_mask, aperture_mask_draw = self.__get_aperture_canvas()
        self.draw_shape(aperture_mask_draw, (255, 255, 255, 255))
        if self.hole_diameter:
            aperture_mask_draw.ellipse(
                self.get_aperture_hole_bbox().as_tuple_y_inverse(),
                (0, 0, 0, 0),
            )
        return aperture_mask

    @cached_property
    def aperture_stamp_dark(self) -> Image.Image:
        aperture_stamp, aperture_stamp_draw = self.__get_aperture_canvas()
        self.draw_shape(aperture_stamp_draw, self.get_dark_color())
        return aperture_stamp

    @cached_property
    def aperture_stamp_clear(self) -> Image.Image:
        aperture_stamp, aperture_stamp_draw = self.__get_aperture_canvas()
        self.draw_shape(aperture_stamp_draw, self.get_clear_color())
        return aperture_stamp

    def draw_shape(self, aperture_stamp_draw: ImageDraw.Draw, color: Tuple):
        raise NotImplementedError(
            f"Implement draw_shape(...) in subclass of {self.__class__.__qualname__}"
        )

    def __get_aperture_canvas(self) -> Image.Image:
        canvas = Image.new(
            "RGBA",
            self.__get_aperture_canvas_size(),
            (0, 0, 0, 0),
        )
        canvas_draw = ImageDraw.Draw(canvas)
        return canvas, canvas_draw

    def __get_aperture_canvas_size(self) -> Tuple[float, float]:
        return int(self.pixel_bbox.width() + 1), int(self.pixel_bbox.height() + 1)

    def get_aperture_bbox(self) -> Tuple[float]:
        return 0, 0, self.pixel_bbox.width() - 1, self.pixel_bbox.height() - 1

    @cached_property
    def pixel_bbox(self):
        bbox = self.bbox()
        return BoundingBox(
            self._prepare_co(bbox.left),
            self._prepare_co(bbox.lower),
            self._prepare_co(bbox.right),
            self._prepare_co(bbox.upper),
        )

    def flash_offset(self):
        return Vector2D(
            self.pixel_bbox.width() / 2, self.pixel_bbox.height() / 2
        ).floor()

    def flash(self, spec: FlashSpec) -> None:
        self.prepare_flash_spec(spec)
        self.flash_at_location(spec.location)

    def flash_at_location(self, location: Vector2D) -> None:
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
