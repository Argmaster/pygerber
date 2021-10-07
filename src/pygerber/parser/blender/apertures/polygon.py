# -*- coding: utf-8 -*-
from __future__ import annotations

from pygerber.parser.blender.apertures.arc_mixin import ArcUtilMixinBlender
from pygerber.parser.blender.apertures.flash_mixin import FlashUtilMixin
from pygerber.renderer.aperture.polygon import PolygonAperture
from pygerber.renderer.spec import ArcSpec
from pygerber.renderer.spec import FlashSpec
from pygerber.renderer.spec import LineSpec


class BlenderPolygon(ArcUtilMixinBlender, FlashUtilMixin, PolygonAperture):
    def flash(self, spec: FlashSpec) -> None:
        pass

    def line(self, spec: LineSpec) -> None:
        pass

    def arc(self, spec: ArcSpec) -> None:
        pass
