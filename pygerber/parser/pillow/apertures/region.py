# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.meta.meta import Interpolation

from pygerber.mathclasses import Vector2D

from typing import List, Tuple

from PIL import Image, ImageDraw
from pygerber.meta.aperture import Aperture, RegionApertureManager
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec, Spec
from pygerber.parser.pillow.apertures.util import PillowUtilMethdos


class PillowRegion(RegionApertureManager, PillowUtilMethdos):
    draw_canvas: ImageDraw.ImageDraw

    def finish(self, bounds: List[Tuple[Aperture, LineSpec]]) -> None:
        if bounds:
            self._draw_region(bounds)

    def _draw_region(self, bounds: List[Tuple[Aperture, LineSpec]]):
        bound_points = []
        for aperture, spec in bounds:
            spec.draw(aperture)
            if isinstance(spec, LineSpec):
                bound_points.append(spec.end.as_tuple())
            elif isinstance(spec, ArcSpec):
                bound_points.extend(self._get_arc_boundpoints(spec))
        self._draw_polygon(bound_points)

    def _get_arc_boundpoints(self, spec: ArcSpec) -> List[Tuple[float, float]]:
        bound_points = []
        for point in self.get_arc_points(spec):
            bound_points.append(point.as_tuple())
        return bound_points

    def _draw_polygon(self, bound_points: List[Tuple[float, float]]):
        self.draw_canvas.polygon(bound_points, self.get_color())
