# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import List
from typing import Tuple

from PyR3.shortcut.mesh import fromPyData
from PyR3.shortcut.modifiers import Solidify

from pygerber.parser.blender.apertures.arc_mixin import ArcUtilMixinBlender
from pygerber.parser.blender.apertures.util import BlenderUtilMethods
from pygerber.renderer.aperture.region import RegionApertureManager
from pygerber.renderer.spec import ArcSpec
from pygerber.renderer.spec import LineSpec


class BlenderRegion(ArcUtilMixinBlender, RegionApertureManager, BlenderUtilMethods):
    def finish(self, bounds: List[LineSpec]) -> None:
        if bounds:
            self.__draw_region(bounds)

    def __draw_region(self, bounds: List[LineSpec]):
        bound_points = []
        for spec in bounds:
            if isinstance(spec, LineSpec):
                bound_points.append(spec.end.as_tuple())
            elif isinstance(spec, ArcSpec):
                bound_points.extend(self.__get_arc_boundpoints(spec))
        self.__create_mesh(bound_points)

    def __get_arc_boundpoints(self, spec: ArcSpec) -> List[Tuple[float, float]]:
        bound_points = []
        for point in self.get_arc_points(spec, self.isCCW):
            bound_points.append(point.as_tuple())
        return bound_points

    def __create_mesh(self, bound_points: List[Tuple[float, float]]):
        vertices = [(x, y, 0) for x, y in bound_points]
        vertex_last_index = len(vertices) - 1
        edges = [(i, i + 1) for i in range(vertex_last_index)] + [
            (vertex_last_index, 0)
        ]
        edge_count = len(edges)
        faces = [tuple(i for i in range(edge_count))]
        mesh_object = fromPyData(
            vertices,
            edges,
            faces,
        )
        self.solidify(mesh_object, self.thickness)
        self.commit_mesh_to_root(mesh_object)
