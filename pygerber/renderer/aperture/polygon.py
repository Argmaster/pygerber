# -*- coding: utf-8 -*-
from __future__ import annotations

from pygerber.tokens.add import ADD_Token
from .circular import CircularAperture


class PolygonAperture(CircularAperture):

    VERTICES: float
    ROTATION: float
    DIAMETER: float
    HOLE_DIAMETER: float

    def __init__(self, args: ADD_Token.ARGS, renderer) -> None:
        super().__init__(args, renderer)
        self.VERTICES = args.VERTICES
        self.ROTATION = args.ROTATION
