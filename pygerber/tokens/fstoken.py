from __future__ import annotations
from functools import cached_property

import re

from .token import Token
from pygerber.exceptions import DeprecatedSyntax


class FormatSpecifierToken(Token):
    regex = re.compile(
        r"%FS(?P<zeros>[LTD])(?P<mode>[AI])X(?P<X_int>[1-6])(?P<X_dec>[1-6])Y(?P<Y_int>[1-6])(?P<Y_dec>[1-6])\*%"
    )

    def zeros(self, value: str) -> str:
        if value == "L":
            return value
        elif not self.meta.ignore_deprecated:
            raise DeprecatedSyntax(
                f"Deprecated zeros format specifier '{value}', only 'L' supported."
            )

    def mode(self, value: str) -> str:
        if value == "A":
            return value
        elif not self.meta.ignore_deprecated:
            raise DeprecatedSyntax(
                f"Deprecated mode format specifier '{value}', only 'A' supported."
            )

    def X_int(self, value: str) -> int:
        X_int = int(value)
        if (
            isinstance(self.Y_int, int)
            and self.Y_int != X_int
            and not self.meta.ignore_deprecated
        ):
            raise DeprecatedSyntax(
                f"Integer format specifier for X and Y are not equal."
            )
        return X_int

    def X_dec(self, value: str) -> int:
        X_dec = int(value)
        if (
            isinstance(self.Y_dec, int)
            and self.Y_dec != X_dec
            and not self.meta.ignore_deprecated
        ):
            raise DeprecatedSyntax(
                f"Decimal format specifier for X and Y are not equal."
            )
        return X_dec

    def Y_int(self, value: str) -> int:
        Y_int = int(value)
        if (
            isinstance(self.X_int, int)
            and self.X_int != Y_int
            and not self.meta.ignore_deprecated
        ):
            raise DeprecatedSyntax(
                f"Integer format specifier for X and Y are not equal."
            )
        return Y_int

    def Y_dec(self, value: str) -> int:
        Y_dec = int(value)
        if (
            isinstance(self.X_dec, int)
            and self.X_dec != Y_dec
            and not self.meta.ignore_deprecated
        ):
            raise DeprecatedSyntax(
                f"Decimal format specifier for X and Y are not equal."
            )
        return Y_dec

    @cached_property
    def length(self):
        return self.X_int + self.X_dec

    @cached_property
    def INT_F(self):
        return self.X_int

    def affect_meta(self):
        self.meta.coparser.set_format(self)

    def __str__(self) -> str:
        return f"FS_Token<{self.zeros}{self.mode}X{self.X_int}{self.X_dec}Y{self.Y_int}{self.Y_dec}>"
