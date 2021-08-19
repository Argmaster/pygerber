# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.meta.data import Vector2D

import re

from pygerber.validators import Coordinate, Int, load_validators

from .token import Token

CO_PATTERN = r"[-+]?[0-9]+"


@load_validators
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

    @property
    def end(self):
        return Vector2D(self.X, self.Y)

    @property
    def offset(self):
        return Vector2D(self.I, self.J)

    def render(self):
        self.meta.draw_interpolated(self.end, self.offset)


@load_validators
class D02_Token(Token):
    regex = re.compile(
        r"(X(?P<X>{0}))?(Y(?P<Y>{0}))?D02\*".format(CO_PATTERN),
    )

    X = Coordinate()
    Y = Coordinate()

    @property
    def point(self):
        return Vector2D(self.X, self.Y)

    def render(self):
        self.meta.move_pointer(self.point)


@load_validators
class D03_Token(Token):
    regex = re.compile(
        r"(X(?P<X>{0}))?(Y(?P<Y>{0}))?D03\*".format(CO_PATTERN),
    )

    X = Coordinate()
    Y = Coordinate()

    @property
    def point(self):
        return Vector2D(self.X, self.Y)

    def render(self):
        self.meta.draw_flash(self.point)


@load_validators
class DNN_Loader_Token(Token):
    regex = re.compile(r"D(?P<ID>[1-9][0-9]*)\*")
    ID = Int()

    def affect_meta(self):
        self.meta.selectAperture(self.ID)
