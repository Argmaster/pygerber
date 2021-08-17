# -*- coding: utf-8 -*-
from __future__ import annotations

import re

from .token import Token
from pygerber.validators import Coordinate, load_validators

CO_PATTERN = r"[-+]?[0-9]+"


@load_validators
class D01_Token(Token):
    regex = re.compile(
        r"(X(?P<X>{0}))?(Y(?P<Y>{0}))?(I(?P<I>{0}))?(J(?P<J>{0}))?D01\*".format(
            CO_PATTERN
        )
    )

    X = Coordinate()
    Y = Coordinate()
    I = Coordinate()
    J = Coordinate()

    def __str__(self) -> str:
        return f"D01_Token<X{self.X}Y{self.Y}I{self.I}J{self.J}>"


@load_validators
class D02_Token(Token):
    regex = re.compile(
        r"(X(?P<X>{0}))?(Y(?P<Y>{0}))?D02\*".format(CO_PATTERN),
    )

    X = Coordinate()
    Y = Coordinate()

    def __str__(self) -> str:
        return f"D02_Token<X{self.X}Y{self.Y}>"


@load_validators
class D03_Token(Token):
    regex = re.compile(
        r"(X(?P<X>{0}))?(Y(?P<Y>{0}))?D03\*".format(CO_PATTERN),
    )

    X = Coordinate()
    Y = Coordinate()

    def __str__(self) -> str:
        return f"D03_Token<X{self.X}Y{self.Y}>"
