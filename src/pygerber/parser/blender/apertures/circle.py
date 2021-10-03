# -*- coding: utf-8 -*-
from __future__ import annotations

import bpy
from PyR3.shortcut.context import Objects
from PyR3.shortcut.mesh import addCircle
from PyR3.shortcut.mesh import fromPyData
from PyR3.shortcut.modifiers import Boolean
from PyR3.shortcut.modifiers import Solidify
from PyR3.shortcut.transform import Transform
from pygerber.mathclasses import Vector2D, angle_from_zero

from pygerber.parser.blender.apertures.arc_mixin import ArcUtilMixinBlender
from pygerber.parser.blender.apertures.flash_mixin import FlashUtilMixin
from pygerber.renderer.aperture.circular import CircularAperture
from pygerber.renderer.spec import ArcSpec
from pygerber.renderer.spec import FlashSpec
from pygerber.renderer.spec import LineSpec


class BlenderCircle(ArcUtilMixinBlender, FlashUtilMixin, CircularAperture):
    @property
    def RADIUS(self):
        return self.DIAMETER / 2

    def create_stamp_shape(self, spec: FlashSpec) -> bpy.types.Object:
        return addCircle(
            radius=self.RADIUS,
            vertices=self.get_number_points_within_angle(radius=self.RADIUS),
            location=spec.location.as_tuple_3D(),
            fill_type="NGON",
        )

    def all_joining_mesh(self, vertices: list) -> bpy.types.Object:
        vertex_last_index = len(vertices) - 1
        edges = [(i, i + 1) for i in range(vertex_last_index)] + [
            (vertex_last_index, 0)
        ]
        edge_count = len(edges)
        faces = [tuple(i for i in range(edge_count))]
        return fromPyData(
            vertices,
            edges,
            faces,
        )

    def line(self, spec: LineSpec) -> None:
        end_point = spec.end - spec.begin
        length = end_point.length()
        left_arc_spec = ArcSpec(
            Vector2D(0, self.RADIUS),
            Vector2D(0, -self.RADIUS),
            Vector2D(0, 0),
        )
        vertices = [p.as_tuple_3D() for p in self.get_arc_points(left_arc_spec, True)]
        right_arc_spec = ArcSpec(
            Vector2D(length, -self.RADIUS),
            Vector2D(length, self.RADIUS),
            Vector2D(length, 0),
        )
        vertices.extend(
            [p.as_tuple_3D() for p in self.get_arc_points(right_arc_spec, True)]
        )
        line_mesh = self.all_joining_mesh(vertices)
        angle = angle_from_zero(end_point)
        Objects.select_only(line_mesh)
        override = bpy.context.copy()
        override["area"] = [a for a in bpy.context.screen.areas if a.type == "VIEW_3D"][
            0
        ]
        bpy.ops.transform.rotate(
            override,
            value=-angle,
            orient_axis="Z",
            orient_type="GLOBAL",
            center_override=(0, 0, 0),
        )
        Transform.move(spec.begin.as_tuple_3D())
        self.solidify(line_mesh, self.thickness)
        self.commit_mesh_to_root(line_mesh)

    def arc(self, spec: ArcSpec) -> None:
        pass
