# -*- coding: utf-8 -*-
from __future__ import annotations

from pygerber.parser.blender.apertures.arc_mixin import ArcUtilMixinBlender
from pygerber.parser.blender.apertures.flash_mixin import FlashUtilMixin
from pygerber.renderer.aperture.circular import CircularAperture
from pygerber.renderer.spec import ArcSpec
from pygerber.renderer.spec import FlashSpec
from pygerber.renderer.spec import LineSpec

from PyR3.shortcut.mesh import addCircle
from PyR3.shortcut.modifiers import Boolean
from PyR3.shortcut.modifiers import Solidify
from PyR3.shortcut.context import Objects
import bpy


class BlenderCircle(ArcUtilMixinBlender, FlashUtilMixin, CircularAperture):
    def create_stamp_shape(self, spec: FlashSpec) -> bpy.types.Object:
        RADIUS = self.DIAMETER / 2
        return addCircle(
            radius=RADIUS,
            vertices=self.get_number_points_within_angle(radius=RADIUS),
            location=spec.location.as_tuple_3D(),
            fill_type="NGON",
        )

    def line(self, spec: LineSpec) -> None:
        pass

    def arc(self, spec: ArcSpec) -> None:
        pass
