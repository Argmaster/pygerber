from __future__ import annotations
from functools import cached_property

import re

from .token import Token


class FormatSpecifierToken(Token):
    regex = re.compile(
        r"%FS(?P<zeros>[LTD])(?P<mode>[AI])X(?P<X_int>[1-6])(?P<X_dec>[1-6])Y(?P<Y_int>[1-6])(?P<Y_dec>[1-6])\*%"
    )

    X_int = int
    X_dec = int
    zeros = str
    mode = str

    def Y_int(self, value: str) -> int:
        Y_int = int(value)
        self.raiseDeprecatedIfNotEqual(
            self.X_int, Y_int, "Integer format specifier for X and Y are not equal."
        )
        return Y_int

    def Y_dec(self, value: str) -> int:
        Y_dec = int(value)
        self.raiseDeprecatedIfNotEqual(
            self.X_dec, Y_dec, f"Decimal format specifier for X and Y are not equal."
        )
        return Y_dec

    def raiseDeprecatedIfNotEqual(self, value_1, value_2, message) -> None:
        if value_1 != value_2:
            self.meta.raise_deprecated_syntax(message)

    @cached_property
    def length(self):
        return self.INT_FORMAT + self.DEC_FORMAT

    @cached_property
    def INT_FORMAT(self):
        return self.X_int

    @cached_property
    def DEC_FORMAT(self):
        return self.X_dec

    def affect_meta(self):
        self.meta.coparser.set_format(self)

    def __str__(self) -> str:
        return f"FS_Token<{self.zeros}{self.mode}X{self.X_int}{self.X_dec}Y{self.Y_int}{self.Y_dec}>"
