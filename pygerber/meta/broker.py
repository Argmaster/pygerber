# -*- coding: utf-8 -*-
from typing import List, Tuple

from .aperture import Aperture, ApertureManager
from .meta import DrawingMeta, TransformMeta
from .spec import ArcSpec, FlashSpec, LineSpec, RegionSpec, Spec
from .data import Vector2D


class DrawingBroker(TransformMeta, DrawingMeta, ApertureManager):
    current_aperture: Aperture
    current_point: Tuple[float, float]

    def draw_flash(self, point: Vector2D) -> None:
        spec = FlashSpec(
            point,
            self.is_regionmode,
        )
        if self.is_regionmode:
            self.pushRegionStep(spec)
        else:
            self.current_aperture.flash(spec)

    def draw_interpolated(self, end: Vector2D, offset: Vector2D) -> None:
        if self.interpolation == DrawingMeta.Interpolation.Linear:
            self.draw_line(end)
        else:
            self.draw_arc(end, offset)

    def draw_line(self, end: Vector2D) -> None:
        spec = LineSpec(
            self.current_point,
            end,
            self.is_regionmode,
        )
        if self.is_regionmode:
            self.pushRegionStep(spec)
        else:
            self.current_aperture.line(spec)

    def draw_arc(self, end: Vector2D, offset: Vector2D) -> None:
        spec = ArcSpec(
            self.current_point,
            end,
            self.current_point + offset,
            self.is_regionmode,
        )
        if self.is_regionmode:
            self.pushRegionStep(spec)
        else:
            self.current_aperture.arc(spec)

    def end_region(self):
        super().end_region()
        apertureClass = self.apertureSet.getApertureClass(None, True)
        apertureClass(STEPS=self.region_bounds).region()
        self.region_bounds = []

    def move_pointer(self, end: Vector2D) -> None:
        self.current_point = self.fill_xy_none_with_current(end)

    def fill_xy_none_with_current(self, point: Vector2D):
        if point.x is None:
            point.x = self.current_point.x
        if point.y is None:
            point.y = self.current_point.y
        return point
