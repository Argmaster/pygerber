# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.validators.coordinate import UnitFloat
from pygerber.validators.struct_validator import StructValidator

if TYPE_CHECKING:
    from pygerber.renderer import Renderer

import re

from pygerber.validators.basic import Float
from pygerber.validators.basic import Int
from pygerber.validators.basic import String

from .token import Token


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

    class ARGS_dispatcher(StructValidator):
        DIAMETER = UnitFloat()
        X = UnitFloat()
        Y = UnitFloat()
        VERTICES = Int()
        ROTATION = Float(0.0)
        HOLE_DIAMETER = UnitFloat(0)

    @ARGS_dispatcher
    def ARGS(self: Token, __: str) -> re.Pattern:
        if self.TYPE == "C":
            return self.CIRCLE_PATTERN
        elif self.TYPE == "R" or self.TYPE == "O":
            return self.RECTANGLE_PATTERN
        elif self.TYPE == "P":
            return self.POLYGON_PATTERN

    def pre_render(self, renderer: Renderer):
        renderer.define_aperture(self.TYPE, self.NAME, self.ID, self.ARGS)
