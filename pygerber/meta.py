# -*- coding: utf-8 -*-
from pygerber.exceptions import DeprecatedSyntax
from pygerber.coparser import CoParser
from typing import Tuple


class TransformMeta:
    class Polarity:
        DARK = "D"
        CLEAR = "C"

    class Mirroring:
        No = "N"
        X = "X"
        Y = "Y"
        XY = "XY"

    polarity: str
    mirroring: str
    rotation: float
    scale: float


class Meta:
    class Unit:
        MILLIMETERS = "MM"
        INCHES = "IN"

    class Interpolation:
        Linear = 1
        ClockwiseCircular = 2
        CounterclockwiseCircular = 3

    def __init__(
        self,
        *,
        ignore_deprecated: bool = True,
        coparser: CoParser = None,
        unit: Unit = Unit.MILLIMETERS,
        current_point: Tuple[float, float] = (0, 0),
        current_aperture: object = None,
        interpolation: Interpolation = Interpolation.Linear,
        is_regionmode: bool = False,
    ) -> None:
        self.ignore_deprecated = ignore_deprecated
        if coparser is None:
            self.coparser = CoParser()
        else:
            self.coparser = coparser
        self.unit = unit
        self.current_point = current_point
        self.current_aperture = current_aperture
        self.interpolation = interpolation
        self.is_regionmode = is_regionmode

    def select_aperture(self, id: int):
        self.current_aperture = id

    def set_interpolation(self, interpolation: Interpolation):
        self.interpolation = interpolation

    def begin_region(self):
        self.is_regionmode = True

    def end_region(self):
        self.is_regionmode = False

    def set_polarity(self, polarity):
        self.polarity = polarity

    def set_rotation(self, angle: float):
        self.rotation = angle

    def set_scaling(self, scale: float):
        self.scale = scale

    def set_mirroring(self, mode):
        self.mirroring = mode

    def set_unit(self, unit):
        self.unit = unit

    def raiseDeprecatedSyntax(self, message: str):
        if not self.ignore_deprecated:
            raise DeprecatedSyntax(message)
