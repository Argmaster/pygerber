# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.mathclasses import Vector2D
from pygerber.meta.spec import LineSpec


LINE_DELTA_STEP = 4


class FlashLineMixin:
    def line(self, spec: LineSpec) -> None:
        self.prepare_line_spec(spec)
        for vec in self.__get_line_flash_offset_vector(spec):
            self.flash_at_location(spec.begin + vec)

    def __get_line_flash_offset_vector(self, spec: LineSpec) -> Vector2D:
        length_vector = spec.end - spec.begin
        length_vector.x = length_vector.x
        length_vector.y = length_vector.y
        no_of_steps = int(length_vector.length())
        step_delta_vector = length_vector / no_of_steps
        for i in range(0, no_of_steps, LINE_DELTA_STEP):
            yield (step_delta_vector * i).floor()
        yield (step_delta_vector * no_of_steps).floor()
