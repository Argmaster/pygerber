# -*- coding: utf-8 -*-
from __future__ import annotations
from math import degrees, radians, cos, sin, tau
from pygerber.mathclasses import Vector2D, angle_from_zero
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
            int(self._prepare_co(vector.x) + self.broker.canvas_width_half),
            int(self._prepare_co(vector.y) + self.broker.canvas_height_half),
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

    def _get_begin_end_angles(self, spec: ArcSpec):
        begin_absolute = spec.begin - spec.center
        end_absolute = spec.end - spec.center
        begin_angle = degrees(angle_from_zero(begin_absolute))
        end_angle = degrees(angle_from_zero(end_absolute))
        return int(begin_angle), int(end_angle)


class PillowFlashArcMixin:

    def _arc_of_flashes(self, spec, begin_angle, end_angle):
        radius = self._get_radius(spec)
        x, y = self._get_arc_co_functions(radius)
        alpha = begin_angle
        delta = self._get_delta(begin_angle, end_angle, radius)
        while alpha <= end_angle:
            self._flash(Vector2D(x(alpha) + spec.center.x, y(alpha) + spec.center.y))
            alpha += delta

    def _get_arc_co_functions(self, radius):
        x = lambda alpha: radius * cos(radians(alpha))
        y = lambda alpha: radius * sin(radians(alpha))
        return x, y

    def _get_radius(self, spec: ArcSpec):
        return (spec.begin - spec.center).length()

    def _get_delta(self, begin_angle, end_angle, radius):
        angle_difference = end_angle - begin_angle
        arc_ratio_of_circle = angle_difference / 360
        arc_length = abs(tau * radius * arc_ratio_of_circle)
        number_of_points = int(arc_length * self.dpmm)
        return angle_difference / number_of_points
