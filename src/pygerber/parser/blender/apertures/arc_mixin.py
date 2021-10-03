# -*- coding: utf-8 -*-
from __future__ import annotations

import math

from pygerber.renderer.arc_util_mixin import ArcUtilMixin


class ArcUtilMixinBlender(ArcUtilMixin):
    def points_in_arc(self, arc_length: float):
        MIN_CIRCLE_POINTS = 9
        POINT_COUNT_MULTIPLIER = 0.9
        point_count = MIN_CIRCLE_POINTS + int(arc_length) * POINT_COUNT_MULTIPLIER
        return point_count

    def get_number_points_within_angle(self, relative_angle=math.pi * 2, radius=1.0):
        arc_ratio = self.get_arc_ratio(relative_angle)
        arc_length = self.get_arc_length(radius) * arc_ratio
        return self.points_in_arc(arc_length)

    def get_arc_traverse_step_angle(self, begin_angle, end_angle, radius):
        relative_angle = self.get_relative_angle(begin_angle, end_angle)
        return relative_angle / self.get_number_points_within_angle(
            relative_angle, radius
        )
