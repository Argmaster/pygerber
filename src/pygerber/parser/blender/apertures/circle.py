# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.parser.blender.apertures.arc_mixin import ArcUtilMixinBlender

from pygerber.renderer.aperture.circular import CircularAperture
from pygerber.renderer.spec import ArcSpec
from pygerber.renderer.spec import LineSpec


class BlenderCircle(ArcUtilMixinBlender, CircularAperture):
    pass
