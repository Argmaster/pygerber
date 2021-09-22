# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING
from pygerber.mathclasses import Vector2D

import re

from pygerber.validators.basic import Int
from pygerber.validators.coordinate import Coordinate
if TYPE_CHECKING:
    from pygerber.renderer import Renderer

from .token import Deprecated, Token

CO_PATTERN = r"[-+]?[0-9]+"


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

    def render(self, renderer: Renderer):
        renderer.draw_interpolated(self.end, self.offset)

    def post_render(self, renderer: Renderer):
        renderer.move_pointer(self.end)

    def bbox(self, renderer: Renderer):
        renderer.bbox_interpolated(self.end, self.offset)


class D02_Token(Token):
    regex = re.compile(
        r"(X(?P<X>{0}))?(Y(?P<Y>{0}))?D02\*".format(CO_PATTERN),
    )

    X = Coordinate()
    Y = Coordinate()

    @property
    def point(self):
        return Vector2D(self.X, self.Y)

    def post_render(self, renderer: Renderer):
        renderer.move_pointer(self.point)


class D03_Token(D02_Token):
    regex = re.compile(
        r"(X(?P<X>{0}))?(Y(?P<Y>{0}))?D03\*".format(CO_PATTERN),
    )

    def render(self, renderer: Renderer):
        renderer.draw_flash(self.point)

    def post_render(self, renderer: Renderer):
        renderer.move_pointer(self.point)

    def bbox(self, renderer: Renderer):
        renderer.bbox_flash(self.point)



class DNN_Loader_Token(Token):
    regex = re.compile(r"D(?P<ID>[1-9][0-9]*)\*")
    ID = Int()

    def pre_render(self, renderer: Renderer):
        renderer.select_aperture(self.ID)

@Deprecated("G54 command is deprecated since 2012")
class G54DNN_Loader_Token(DNN_Loader_Token):
    regex = re.compile(r"G54D(?P<ID>[1-9][0-9]*)\*")
