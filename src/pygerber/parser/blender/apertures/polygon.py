# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.parser.blender.apertures.arc_mixin import ArcUtilMixinBlender

from pygerber.renderer.aperture.polygon import PolygonAperture
from pygerber.renderer.spec import ArcSpec
from pygerber.renderer.spec import LineSpec


class BlenderPolygon(ArcUtilMixinBlender, PolygonAperture):
    pass
