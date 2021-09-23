# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygerber.renderer import Renderer
    from pygerber.drawing_state import DrawingState
from pygerber.mathclasses import BoundingBox, Vector2D

import re


from .dispatcher_meta import Dispatcher


class Token(Dispatcher):
    regex: re.Pattern
    re_match: re.Match
    keep: bool = True
    __deprecated__: bool = False
    renderer: Renderer = None

    def alter_state(self, state: DrawingState):
        """
        This method should be called before render().
        """
        pass

    def pre_render(self, renderer: Renderer):
        # called right before render, even if render was not called
        pass

    def render(self, renderer: Renderer):
        """
        This method should be called only after token is dispatched and after alter_state().
        """
        pass

    def post_render(self, renderer: Renderer):
        # called right after render, even if render was not called
        pass

    def bbox(self) -> BoundingBox:
        pass

    def __str__(self) -> str:
        """
        Construct string of Gerber code coresponding to data held in token.
        """
        return self.re_match.group()


class Deprecated:
    def __init__(self, message) -> None:
        self.message = message

    def __call__(self, class_: Token):
        message = self.message
        class_.__deprecated__ = message
        return class_
