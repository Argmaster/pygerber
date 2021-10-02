# -*- coding: utf-8 -*-
from __future__ import annotations

from pygerber.renderer.arc_util_mixin import ArcUtilMixin


class ArcUtilMixinBlender(ArcUtilMixin):
    def get_arc_traverse_step_angle(self, begin_angle, end_angle, radius):
        relative_angle = self.get_relative_angle(begin_angle, end_angle)
        arc_ratio = self.get_arc_ratio(relative_angle)
        arc_length = self.get_arc_length(radius) * arc_ratio
        # TODO number_of_points should depend on arc_length
        number_of_points = 256
        return relative_angle / number_of_points
