# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.meta.meta import Unit

import re

from pygerber.validators import Int, load_validators

from .token import Deprecated, Token


@load_validators
class G0N_Token(Token):
    regex = re.compile(r"G0(?P<INTERPOLATION>[1-3])\*?")

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

@Deprecated("G55 command is deprecated since 2012")
@load_validators
class G55_Token(Token):
    regex = re.compile(r"G55.*?\*")

@Deprecated("G70 command is deprecated since 2012")
@load_validators
class G70_Token(Token):
    regex = re.compile(r"G70.*?\*")

    def affect_meta(self):
        self.meta.set_unit(Unit.INCHES)


@Deprecated("G71 command is deprecated since 2012")
@load_validators
class G71_Token(Token):
    regex = re.compile(r"G71.*?\*")

    def affect_meta(self):
        self.meta.set_unit(Unit.MILLIMETERS)


@Deprecated("G90 command is deprecated since 2012")
@load_validators
class G90_Token(Token):
    regex = re.compile(r"G90\*")

    def affect_meta(self):
        self.meta.coparser.set_mode("A")


@Deprecated("G91 command is deprecated since 2012")
@load_validators
class G91_Token(Token):
    regex = re.compile(r"G91\*")

    def affect_meta(self):
        self.meta.coparser.set_mode("I")
