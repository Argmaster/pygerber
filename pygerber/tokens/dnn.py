# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.mathclasses import Vector2D

import re

from pygerber.validators import Int, load_validators, OffsetCoordinate, VectorCoordinateX, VectorCoordinateY

from .token import Deprecated, Token

CO_PATTERN = r"[-+]?[0-9]+"


@load_validators
class D01_Token(Token):
    regex = re.compile(
        r"(X(?P<X>{0}))?(Y(?P<Y>{0}))?(I(?P<I>{0}))?(J(?P<J>{0}))?D01\*".format(
            CO_PATTERN
        )
    )

    X = VectorCoordinateX()
    Y = VectorCoordinateY()
    I = OffsetCoordinate()
    J = OffsetCoordinate()

    @property
    def end(self):
        return Vector2D(self.X, self.Y)

    @property
    def offset(self):
        return Vector2D(self.I, self.J)

    def render(self):
        self.meta.draw_interpolated(self.end, self.offset)

    def post_render(self):
        self.meta.move_pointer(self.end)

    def bbox(self):
        return self.meta.bbox_interpolated(self.end, self.offset)


@load_validators
class D02_Token(Token):
    regex = re.compile(
        r"(X(?P<X>{0}))?(Y(?P<Y>{0}))?D02\*".format(CO_PATTERN),
    )

    X = VectorCoordinateX()
    Y = VectorCoordinateY()

    @property
    def point(self):
        return Vector2D(self.X, self.Y)

    def post_render(self):
        self.meta.move_pointer(self.point)


@load_validators
class D03_Token(Token):
    regex = re.compile(
        r"(X(?P<X>{0}))?(Y(?P<Y>{0}))?D03\*".format(CO_PATTERN),
    )

    X = VectorCoordinateX()
    Y = VectorCoordinateY()

    @property
    def point(self):
        return Vector2D(self.X, self.Y)

    def render(self):
        self.meta.draw_flash(self.point)

    def post_render(self):
        self.meta.move_pointer(self.point)

    def bbox(self):
        return self.meta.bbox_flash(self.point)


@Deprecated("G54 command is deprecated since 2012")
@load_validators
class G54DNN_Loader_Token(Token):
    regex = re.compile(r"G54D(?P<ID>[1-9][0-9]*)\*")
    ID = Int()

    def affect_meta(self):
        self.meta.select_aperture(self.ID)


@load_validators
class DNN_Loader_Token(Token):
    regex = re.compile(r"D(?P<ID>[1-9][0-9]*)\*")
    ID = Int()

    def affect_meta(self):
        self.meta.select_aperture(self.ID)