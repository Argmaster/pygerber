# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.constants import Interpolation, Mirroring, Polarity, Unit

from .coparser import CoParser

if TYPE_CHECKING:
    from pygerber.tokens.fs import FormatSpecifierToken


class DrawingState:

    mirroring: str
    rotation: float
    scale: float

    unit: Unit
    polarity: str
    interpolation: Interpolation
    is_regionmode: bool
    coparser: CoParser

    def __init__(self) -> None:
        self.set_defaults()

    def set_defaults(self):
        self.coparser = CoParser()
        self.mirroring = Mirroring.No
        self.rotation = 0.0
        self.scale = 1.0
        self.is_regionmode = False
        self.unit = Unit.MILLIMETERS
        self.polarity = Polarity.DARK
        self.interpolation = Interpolation.Linear

    def parse_co(self, float_string: str):
        return self.coparser.parse(float_string)

    def set_co_format(self, fs: FormatSpecifierToken):
        return self.coparser.set_format(fs)

    def set_rotation(self, angle: float):
        self.rotation = angle

    def set_scaling(self, scale: float):
        self.scale = scale

    def set_mirroring(self, mode):
        self.mirroring = mode

    def set_unit(self, unit):
        self.unit = unit

    def set_polarity(self, polarity):
        self.polarity = polarity

    def set_interpolation(self, interpolation):
        self.interpolation = interpolation

    def begin_region(self):
        self.is_regionmode = True

    def end_region(self):
        self.is_regionmode = False
