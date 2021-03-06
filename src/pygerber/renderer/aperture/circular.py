# -*- coding: utf-8 -*-
from __future__ import annotations

from pygerber.mathclasses import BoundingBox
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
