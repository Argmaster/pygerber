from __future__ import annotations

import re
from typing import Union

from .token import Token


class D01_Token(Token):
    regex = re.compile(
        r"(X(?P<X>[-+]?[0-9]+))?(Y(?P<Y>[-+]?[0-9]+))?(I(?P<I>[-+]?[0-9]+))?(J(?P<J>[-+]?[0-9]+))?D01\*"
    )

    def parse_float(self, value: Union[str, None]) -> float:
        if value is not None:
            return self.meta.coparser.parse(value)

    X = parse_float
    Y = parse_float
    I = parse_float
    J = parse_float

    def __str__(self) -> str:
        return f"D01_Token<X{self.X}Y{self.Y}I{self.I}J{self.J}>"


class D02_Token(Token):
    regex = re.compile(r"(X(?P<X>[-+]?[0-9]+))?(Y(?P<Y>[-+]?[0-9]+))?D02")

    def parse_float(self, value: Union[str, None]) -> float:
        if value is not None:
            return self.meta.coparser.parse(value)

    X = parse_float
    Y = parse_float

    def __str__(self) -> str:
        return f"D02_Token<X{self.X}Y{self.Y}>"
