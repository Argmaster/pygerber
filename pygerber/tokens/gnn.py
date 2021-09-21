# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.mathclasses import BoundingBox

import re

from pygerber.validators.basic import Int

from .token import Deprecated, Token


class G0N_Token(Token):
    regex = re.compile(r"G0(?P<INTERPOLATION>[1-3])\*?")

    INTERPOLATION = Int()

    def alter_state(self):
        self.meta.set_interpolation(self.INTERPOLATION)


class G36_Token(Token):
    regex = re.compile(r"G36\*")

    def alter_state(self):
        self.meta.begin_region()


class G37_Token(Token):
    regex = re.compile(r"G37\*")

    def alter_state(self):
        self.manager, self.bounds = self.meta.finish_drawing_region()

    def render(self):
        self.manager.finish(self.bounds)

    def post_render(self):
        self.meta.end_region()

    def bbox(self) -> BoundingBox:
        return self.manager.bbox(self.bounds)


@Deprecated("G55 command is deprecated since 2012")
class G55_Token(Token):
    regex = re.compile(r"G55.*?\*")


@Deprecated("G70 command is deprecated since 2012")
class G70_Token(Token):
    regex = re.compile(r"G70.*?\*")

    def alter_state(self):
        self.meta.set_unit(Unit.INCHES)


@Deprecated("G71 command is deprecated since 2012")
class G71_Token(Token):
    regex = re.compile(r"G71.*?\*")

    def alter_state(self):
        self.meta.set_unit(Unit.MILLIMETERS)


@Deprecated("G90 command is deprecated since 2012")
class G90_Token(Token):
    regex = re.compile(r"G90\*")

    def alter_state(self):
        self.meta.coparser.set_mode("A")


@Deprecated("G91 command is deprecated since 2012")
class G91_Token(Token):
    regex = re.compile(r"G91\*")

    def alter_state(self):
        self.meta.coparser.set_mode("I")
