# -*- coding: utf-8 -*-
from __future__ import annotations

from pygerber.renderer.arc_util_mixin import ArcUtilMixin


class ArcUtilMixinPillow(ArcUtilMixin):

    dpmm: float

    def get_arc_traverse_step_angle(self, begin_angle, end_angle, radius):
        relative_angle = self.get_relative_angle(begin_angle, end_angle)
        arc_ratio = self.get_arc_ratio(relative_angle)
        arc_length = self.get_arc_length(radius) * arc_ratio
        number_of_points = int(arc_length * self.dpmm)
        return relative_angle / number_of_points
