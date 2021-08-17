# -*- coding: utf-8 -*-
from __future__ import annotations

import re

from pygerber.validators import Int, load_validators

from .token import Token


@load_validators
class G0N_Token(Token):
    regex = re.compile(r"G0(?P<INTERPOLATION>[1-3])\*")

    INTERPOLATION = Int()

    def affect_meta(self):
        self.meta.set_interpolation(self.INTERPOLATION)


@load_validators
class G36_Token(Token):
    regex = re.compile(r"G36\*")

    def affect_meta(self):
        self.meta.begin_region()


@load_validators
class G37_Token(Token):
    regex = re.compile(r"G37\*")

    def affect_meta(self):
        self.meta.end_region()
