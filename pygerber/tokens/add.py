# -*- coding: utf-8 -*-
from __future__ import annotations

import re

from .token import Token
from pygerber.validators import Dispatcher, Float, Int, String, load_validators


@load_validators
class ADD_Token(Token):

    FLOAT_PATTERN = r"[-+]?[0-9]*\.?[0-9]*"

    CIRCLE_PATTERN = re.compile(
        r"(?P<DIAMETER>{0})(X(?P<HOLE_DIAMETER>{0}))?".format(FLOAT_PATTERN)
    )
    RECTANGLE_PATTERN = re.compile(
        r"(?P<X>{0})X(?P<Y>{0})(X(?P<HOLE_DIAMETER>{0}))?".format(FLOAT_PATTERN)
    )
    POLYGON_PATTERN = re.compile(
        (
            r"(?P<DIAMETER>{0})X(?P<VERTICES>{0})(X(?P<ROTATION>{0}))?(X(?P<HOLE_DIAMETER>{0}))?"
        ).format(FLOAT_PATTERN)
    )

    BASIC_APERTURE = r"(?P<TYPE>[CROP]),(?P<ARGS>({0}X?)+)".format(FLOAT_PATTERN)
    NAMED_APERTURE = r"(?P<NAME>[a-zA-Z0-9]+)"
    regex = re.compile(
        r"%ADD(?P<ID>[0-9]+)({0}|{1})\*%".format(
            BASIC_APERTURE,
            NAMED_APERTURE,
        )
    )

    ID = Int()
    TYPE = String()
    NAME = String()

    @load_validators
    class ARGS_dispatcher(Dispatcher):
        DIAMETER = Float()
        X = Float()
        Y = Float()
        VERTICES = Int()
        ROTATION = Float(0.0)
        HOLE_DIAMETER = Float(0.0)

    @ARGS_dispatcher
    def ARGS(self: Token, __: str) -> re.Pattern:
        if self.TYPE == "C":
            return self.CIRCLE_PATTERN
        elif self.TYPE == "R" or self.TYPE == "O":
            return self.RECTANGLE_PATTERN
        elif self.TYPE == "P":
            return self.POLYGON_PATTERN

    def affect_meta(self):
        self.meta.defineAperture(self)
