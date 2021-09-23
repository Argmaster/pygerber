# -*- coding: utf-8 -*-
from __future__ import annotations

from pygerber.mathclasses import BoundingBox
from pygerber.tokens.add import ADD_Token
from .aperture import Aperture


class RectangularAperture(Aperture):

    X: float
    Y: float
    HOLE_DIAMETER: float

    def __init__(self, args: ADD_Token.ARGS, renderer) -> None:
        self.renderer = renderer
        self.X = args.X
        self.Y = args.Y
        self.HOLE_DIAMETER = args.HOLE_DIAMETER

    def bbox(self) -> BoundingBox:
        x_half = self.X / 2
        y_half = self.Y / 2
        return BoundingBox(
            -x_half,
            y_half,
            x_half,
            -y_half,
        )
