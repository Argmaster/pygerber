# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.parser.blender.apertures.arc_mixin import ArcUtilMixinBlender

from pygerber.renderer.aperture.rectangular import RectangularAperture
from pygerber.renderer.spec import ArcSpec
from pygerber.renderer.spec import LineSpec


class BlenderRectangle(ArcUtilMixinBlender, RectangularAperture):
    pass
