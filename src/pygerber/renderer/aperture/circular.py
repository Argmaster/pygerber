# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Tuple

from pygerber.mathclasses import BoundingBox
from pygerber.renderer.arc_util_mixin import ArcUtilMixin
from pygerber.renderer.spec import ArcSpec
from pygerber.renderer.spec import FlashSpec
from pygerber.renderer.spec import LineSpec
from pygerber.renderer.spec import Spec
from pygerber.tokens.add import ADD_Token

from .aperture import Aperture


class CircularAperture(Aperture):

    DIAMETER: float
    HOLE_DIAMETER: float

    def __init__(self, args: ADD_Token.ARGS, renderer) -> None:
        self.renderer = renderer
        self.HOLE_DIAMETER = args.HOLE_DIAMETER
        self.DIAMETER = args.DIAMETER

    def bbox(self) -> BoundingBox:
        d_half = self.DIAMETER / 2
        return BoundingBox(
            -d_half,
            d_half,
            d_half,
            -d_half,
        )
