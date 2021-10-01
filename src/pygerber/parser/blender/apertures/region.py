# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.parser.blender.apertures.arc_mixin import ArcUtilMixinBlender
from pygerber.parser.blender.apertures.util import BlenderUtilMethods

from pygerber.renderer.aperture.region import RegionApertureManager


class BlenderRegion(ArcUtilMixinBlender, RegionApertureManager, BlenderUtilMethods):
    pass
