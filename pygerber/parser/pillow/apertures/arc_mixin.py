# -*- coding: utf-8 -*-
from __future__ import annotations

from math import tau

from pygerber.meta.arc_util_mixin import ArcUtilMixin


class ArcUtilMixinPillow(ArcUtilMixin):
    def get_arc_traverse_step_angle(self, begin_angle, end_angle, radius):
        relative_angle = self.get_relative_angle(begin_angle, end_angle)
        arc_ratio = self.get_arc_ratio(relative_angle)
        arc_length = self.get_arc_length(radius) * arc_ratio
        # TODO self.dpmm shouldn't be used there
        number_of_points = int(arc_length * self.dpmm)
        return relative_angle / number_of_points

    @staticmethod
    def get_arc_length(radius) -> float:
        return tau * radius

    @staticmethod
    def get_arc_ratio(relative_angle):
        return relative_angle / 360

    @staticmethod
    def get_relative_angle(begin_angle, end_angle):
        return end_angle - begin_angle
