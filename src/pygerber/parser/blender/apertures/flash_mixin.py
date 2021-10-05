# -*- coding: utf-8 -*-
from __future__ import annotations

import bpy
from PyR3.shortcut.context import Objects
from PyR3.shortcut.mesh import addCircle
from PyR3.shortcut.modifiers import Boolean

from pygerber.parser.blender.apertures.util import BlenderUtilMethods
from pygerber.renderer.spec import FlashSpec


class FlashUtilMixin(BlenderUtilMethods):

    def flash(self, spec: FlashSpec) -> None:
        shape = self.create_stamp_shape(spec)
        self.solidify(shape, self.thickness)
        if self.HOLE_DIAMETER > 0:
            self.make_hole_in_stamp(spec, shape)
        self.commit_mesh_to_root(shape)

    def make_hole_in_stamp(self, spec, shape):
        HOLE_RADIUS = self.HOLE_DIAMETER / 2
        hole_shape = addCircle(
                radius=HOLE_RADIUS,
                vertices=self.get_number_points_within_angle(radius=HOLE_RADIUS),
                location=spec.location.as_tuple_3D(),
                fill_type="NGON",
            )
        self.solidify(hole_shape, self.inner_thickness)
        Boolean(shape, hole_shape, "DIFFERENCE").apply()
        Objects.delete(hole_shape)

    def create_stamp_shape(self) -> bpy.types.Object:
        raise NotImplementedError(
            "Implement create_stamp_shape() in subclass of FlashUtilMixin."
        )
