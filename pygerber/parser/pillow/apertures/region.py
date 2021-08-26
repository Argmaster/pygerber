# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import List, Tuple

from PIL import Image, ImageDraw
from pygerber.meta.aperture import Aperture, RegionApertureManager
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec, Spec
from pygerber.parser.pillow.apertures.util import PillowUtilMethdos


class PillowRegion(RegionApertureManager, PillowUtilMethdos):
    draw_canvas: ImageDraw.ImageDraw

    def finish(self, bounds: List[Tuple[Aperture, Spec]]) -> None:
        pass
