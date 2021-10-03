# -*- coding: utf-8 -*-
from __future__ import annotations

from pygerber.renderer.arc_util_mixin import ArcUtilMixin


class ArcUtilMixinBlender(ArcUtilMixin):
    def points_in_arc(self, arc_length: float):
        MIN_CIRCLE_POINTS = 9
        POINT_COUNT_MULTIPLIER = 1.33
        point_count = max(int(arc_length) * POINT_COUNT_MULTIPLIER, MIN_CIRCLE_POINTS)
        return point_count

    def get_points_within_angle(self, relative_angle, radius):
        arc_ratio = self.get_arc_ratio(relative_angle)
        arc_length = self.get_arc_length(radius) * arc_ratio
        self.points_in_arc(arc_length)

    def get_arc_traverse_step_angle(self, begin_angle, end_angle, radius):
        relative_angle = self.get_relative_angle(begin_angle, end_angle)
        return relative_angle / self.get_points_within_angle(relative_angle, radius)
