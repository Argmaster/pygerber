# -*- coding: utf-8 -*-
from __future__ import annotations

import bpy

from pygerber.parser.blender.apertures.arc_mixin import ArcUtilMixinBlender
from pygerber.parser.blender.apertures.flash_mixin import FlashUtilMixin
from pygerber.renderer.aperture.rectangular import RectangularAperture
from pygerber.renderer.spec import ArcSpec
from pygerber.renderer.spec import FlashSpec
from pygerber.renderer.spec import LineSpec
from PyR3.shortcut.mesh import fromPyData
from PyR3.shortcut.transform import Transform
from PyR3.shortcut.context import Objects


class BlenderRectangle(ArcUtilMixinBlender, FlashUtilMixin, RectangularAperture):
    def create_stamp_shape(self, spec: FlashSpec) -> bpy.types.Object:
        x = self.X / 2
        y = self.Y / 2
        ob = fromPyData(
            [(x, y, 0), (-x, y, 0), (-x, -y, 0), (x, -y, 0)],
            [(0, 1), (1, 2), (2, 3), (3, 0)],
            [(0, 1, 2, 3)],
        )
        Objects.select_only(ob)
        Transform.move(spec.location.as_tuple_3D())
        return ob

    def line(self, spec: LineSpec) -> None:
        pass

    def arc(self, spec: ArcSpec) -> None:
        pass
