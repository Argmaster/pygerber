# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import List, Tuple

from PIL import ImageDraw

from pygerber.parser.pillow.apertures.arc_mixin import ArcUtilMixinPillow
from pygerber.parser.pillow.apertures.util import PillowUtilMethdos
from pygerber.renderer.aperture import RegionApertureManager
from pygerber.renderer.spec import ArcSpec, LineSpec


class PillowRegion(ArcUtilMixinPillow, RegionApertureManager, PillowUtilMethdos):
    draw_canvas: ImageDraw.ImageDraw

    def finish(self, bounds: List[LineSpec]) -> None:
        if bounds:
            self.__draw_region(bounds)

    def __draw_region(self, bounds: List[LineSpec]):
        bound_points = []
        for spec in bounds:
            if isinstance(spec, LineSpec):
                self.prepare_line_spec(spec)
                bound_points.append(spec.end.as_tuple())
            elif isinstance(spec, ArcSpec):
                self.prepare_arc_spec(spec)
                bound_points.extend(self.__get_arc_boundpoints(spec))
        self.__draw_polygon(bound_points)

    def __get_arc_boundpoints(self, spec: ArcSpec) -> List[Tuple[float, float]]:
        bound_points = []
        for point in self.get_arc_points(spec, self.isCCW):
            bound_points.append(point.as_tuple())
        return bound_points

    def __draw_polygon(self, bound_points: List[Tuple[float, float]]):
        self.draw_canvas.polygon(bound_points, self.get_color())
