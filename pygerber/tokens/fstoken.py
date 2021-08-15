from __future__ import annotations

import re

from .token import Token


class FormatSpecifierToken(Token):
    regex = re.compile(
        r"%FS(?P<zeros>[LTD])(?P<mode>[AI])X(?P<X_int>[1-6])(?P<X_dec>[1-6])Y(?P<Y_int>[1-6])(?P<Y_dec>[1-6])\*%"
    )

    def zeros(self, value) -> str:
        if value == "L":
            return value
        elif value == "T" or  value == "D":
            raise
    zeros = str
    mode = str
    X_int = int
    X_dec = int
    Y_int = int
    Y_dec = int

    def affect_meta(self):
        self.meta.coparser.set_format(self)

    def __str__(self) -> str:
        return f"FS_Token<{self.zeros}{self.mode}X{self.X_int}{self.X_dec}Y{self.Y_int}{self.Y_dec}>"
