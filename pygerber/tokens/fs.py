# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from functools import cached_property

from pygerber.validators import CallOnCondition, Int, String, load_validators

from .token import Token


@load_validators
class FormatSpecifierToken(Token):
    regex = re.compile(
        r"%FS(?P<zeros>[LTD])(?P<mode>[AI])X(?P<X_int>[1-6])(?P<X_dec>[1-6])Y(?P<Y_int>[1-6])(?P<Y_dec>[1-6])\*%"
    )

    X_int = Int(3)
    X_dec = Int(6)
    Y_int = CallOnCondition(
        Int(3),
        lambda token, value: token.X_int != value,
        lambda token, _: token.meta.raiseDeprecatedSyntax(
            "Integer format specifier for X and Y are not equal."
        ),
    )
    Y_dec = CallOnCondition(
        Int(6),
        lambda token, value: token.X_dec != value,
        lambda token, _: token.meta.raiseDeprecatedSyntax(
            "Decimal format specifier for X and Y are not equal."
        ),
    )
    zeros = String("L")
    mode = String("A")

    def raiseDeprecatedIfNotEqual(self, value_1, value_2, message) -> None:
        if value_1 != value_2:
            self.meta.raiseDeprecatedSyntax(message)

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
