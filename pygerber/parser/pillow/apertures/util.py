# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.mathclasses import Vector2D
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec
from pygerber.meta.broker import DrawingBroker
from pygerber.meta.meta import Polarity

INCH_TO_MM_MULTIPLIER = 0.0393701


class PillowUtilMethdos:

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
        if self.broker.is_regionmode:
            return self.broker.colors.region
        if self.broker.polarity == Polarity.CLEAR:
            return self.broker.colors.clear
        else:
            return self.broker.colors.dark

    def _prepare_co(self, value: float) -> float:
        return value * self.dpmm

    def prepare_coordinates(self, vector: Vector2D) -> Vector2D:
        return Vector2D(
            int(self._prepare_co(vector.x) + self.broker.canvas.width / 2),
            int(self._prepare_co(vector.y) + self.broker.canvas.height / 2),
        )

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
