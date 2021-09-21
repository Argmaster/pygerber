# -*- coding: utf-8 -*-
from __future__ import annotations

from math import cos, degrees, radians, sin

from pygerber.mathclasses import Vector2D, angle_from_zero
from pygerber.renderer.spec import ArcSpec


DELTA_MULTIPLIER = 25

class ArcUtilMixin:

    @property
    def isCCW(self):
        return self.broker.isCCW()

    def get_begin_end_angles(self, spec: ArcSpec):
        begin_relative = spec.begin - spec.center
        end_relative = spec.end - spec.center
        begin_angle = degrees(angle_from_zero(begin_relative))
        end_angle = degrees(angle_from_zero(end_relative))
        if begin_angle >= end_angle:
            end_angle += 360
        return begin_angle, end_angle

    def get_arc_points(self, spec) -> Vector2D:
        begin_angle, end_angle = self.get_begin_end_angles(spec)
        radius = spec.get_radius()
        x, y = self.get_arc_co_functions(radius)
        delta = self.get_arc_traverse_step_angle(begin_angle, end_angle, radius) * DELTA_MULTIPLIER
        if self.isCCW:
            return self.__get_arc_points_ccw(end_angle, begin_angle, x, spec, y, delta)
        else:
            return self.__get_arc_points_cw(end_angle, begin_angle, x, spec, y, delta)

    def get_arc_traverse_step_angle(self, begin_angle, end_angle, radius):
        raise NotImplementedError("get_arc_traverse_step_angle() have to be implemented in subclass.")

    def __get_arc_points_ccw(self, end_angle, begin_angle, x, spec, y, delta):
        end_relative_angle = end_angle - begin_angle
        angle_offset = begin_angle
        current_angle = 0
        while current_angle <= end_relative_angle:
            yield Vector2D(
                x(current_angle + angle_offset) + spec.center.x,
                y(current_angle + angle_offset) + spec.center.y,
            )
            current_angle += delta

    def __get_arc_points_cw(self, end_angle, begin_angle, x, spec, y, delta):
        end_relative_angle = end_angle - begin_angle
        angle_offset = begin_angle
        current_angle = 360
        while current_angle >= end_relative_angle:
            yield Vector2D(
                x(current_angle + angle_offset) + spec.center.x,
                y(current_angle + angle_offset) + spec.center.y,
            )
            current_angle -= delta

    @staticmethod
    def get_arc_co_functions(radius):
        x = lambda alpha: radius * cos(radians(alpha))
        y = lambda alpha: radius * sin(radians(alpha))
        return x, y
