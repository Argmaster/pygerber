from __future__ import annotations

import re

from .token import Token
from .validator import Float, Int, String


class ADD_Token(Token):

    FLOAT_PATTERN = r"[-+]?[0-9]*.[0-9]*"
    HOLE_DIAMETER_PATTERN = r"(X(?P<HOLE_DIAMETER>{0}))?".format(FLOAT_PATTERN)

    CIRCLE_PATTERN = r"(?P<DIAMETER>{0})".format(FLOAT_PATTERN)
    RECTANGLE_PATTERN = r"(?P<X>{0})X(?P<Y>{0})".format(FLOAT_PATTERN)
    POLYGON_PATTERN = (
        r"(?P<OUTER_DIAMETER>{0})X(?P<VERTICES>{0})(X(?P<ROTATION>{0}))?".format(
            FLOAT_PATTERN
        )
    )
    BASIC_APERTURE = r"(?P<TYPE>[CROP]),({0})|({1})|({2}){3}".format(
        CIRCLE_PATTERN,
        RECTANGLE_PATTERN,
        POLYGON_PATTERN,
        HOLE_DIAMETER_PATTERN,
    )
    regex = re.compile(
        r"%ADD(?P<ID>[0-9]+)({0})|(?P<NAME>[a-zA-Z0-9]+)\*%".format(BASIC_APERTURE)
    )

    ID = Int(0)
    TYPE = String("")
    NAME = String("")
    X = Float(0.0)
    Y = Float(0.0)
    VERTICES = Int(0)
    DIAMETER = Float(0.0)
    HOLE_DIAMETER = Float(0.0)
    OUTER_DIAMETER = Float(0.0)
    ROTATION = Float(0.0)

    def __str__(self) -> str:
        return f"ADD_Token<ID={self.ID}, TYPE={self.TYPE}, NAME={self.NAME}>"
