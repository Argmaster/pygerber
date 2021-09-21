# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from functools import cached_property
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pygerber.drawing_state import DrawingState

from pygerber.validators.basic import Int, String
from pygerber.validators.conditional import CallOnCondition


from .token import Token


class FormatSpecifierToken(Token):
    regex = re.compile(
        r"%FS(?P<zeros>[LTD])(?P<mode>[AI])X(?P<X_int>[1-6])(?P<X_dec>[1-6])Y(?P<Y_int>[1-6])(?P<Y_dec>[1-6])\*%"
    )

    X_int = Int(3)
    X_dec = Int(6)
    Y_int = CallOnCondition(
        Int(3),
        lambda token, value: token.X_int != value,
        lambda token, _: setattr(
            token,
            "__deprecated__",
            "Integer format specifier for X and Y are not equal.",
        ),
    )
    Y_dec = CallOnCondition(
        Int(6),
        lambda token, value: token.X_dec != value,
        lambda token, _: setattr(
            token,
            "__deprecated__",
            "Decimal format specifier for X and Y are not equal.",
        ),
    )
    zeros = String("L")
    mode = String("A")

    @cached_property
    def length(self):
        return self.INT_FORMAT + self.DEC_FORMAT

    @cached_property
    def INT_FORMAT(self):
        return self.X_int

    @cached_property
    def DEC_FORMAT(self):
        return self.X_dec

    def alter_state(self, state: DrawingState):
        state.set_co_format(self)
