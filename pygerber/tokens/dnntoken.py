from __future__ import annotations

import re

from .token import Token
from .validator import Coordinate

CO_PATTERN = r"[-+]?[0-9]+"


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


class D02_Token(D01_Token):
    regex = re.compile(
        r"(X(?P<X>{0}))?(Y(?P<Y>{0}))?D02\*".format(CO_PATTERN),
    )

    def __str__(self) -> str:
        return f"D02_Token<X{self.X}Y{self.Y}>"


class D03_Token(D02_Token):
    regex = re.compile(
        r"(X(?P<X>{0}))?(Y(?P<Y>{0}))?D03\*".format(CO_PATTERN),
    )

    def __str__(self) -> str:
        return f"D03_Token<X{self.X}Y{self.Y}>"
