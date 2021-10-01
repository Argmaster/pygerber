# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import List
from pygerber.parser.blender.apertures.arc_mixin import ArcUtilMixinBlender
from pygerber.parser.blender.apertures.util import BlenderUtilMethods

from pygerber.renderer.aperture.region import RegionApertureManager
from pygerber.renderer.spec import Spec


class BlenderRegion(ArcUtilMixinBlender, RegionApertureManager, BlenderUtilMethods):
    def finish(self, bounds: List[Spec]) -> None:
        pass
