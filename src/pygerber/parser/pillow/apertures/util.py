# -*- coding: utf-8 -*-
from __future__ import annotations

from pygerber.constants import Polarity
from pygerber.mathclasses import Vector2D
from pygerber.renderer import Renderer
from pygerber.renderer.spec import ArcSpec
from pygerber.renderer.spec import FlashSpec
from pygerber.renderer.spec import LineSpec

INCH_TO_MM_MULTIPLIER = 0.0393701


class PillowUtilMethdos:

    renderer: Renderer

    @property
    def dpmm(self):
        return self.renderer.dpmm

    @property
    def canvas(self):
        return self.renderer.canvas

    @property
    def draw_canvas(self):
        return self.renderer.draw_canvas

    def get_color(self):
        if self.is_clear():
            return self.get_clear_color()
        else:
            return self.get_dark_color()

    def is_clear(self):
        return self.renderer.state.polarity == Polarity.CLEAR

    def get_dark_color(self):
        return self.renderer.colors.dark

    def get_clear_color(self):
        return self.renderer.colors.clear

    def prepare_coordinates(self, vector: Vector2D) -> Vector2D:
        return Vector2D(
            int(self._prepare_co(vector.x) + self.renderer.left_offset),
            int(self._prepare_co(vector.y) + self.renderer.bottom_offset),
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
