# -*- coding: utf-8 -*-


class Polarity:
    DARK = "D"
    CLEAR = "C"


class Unit:
    MILLIMETERS = "MM"
    INCHES = "IN"


class Interpolation:
    Linear = 1
    ClockwiseCircular = 2
    CounterclockwiseCircular = 3


class Mirroring:
    No = "N"
    X = "X"
    Y = "Y"
    XY = "XY"


class DrawingMeta:

    unit: Unit
    polarity: str
    interpolation: Interpolation
    is_regionmode: bool

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


class TransformMeta:

    mirroring: str
    rotation: float
    scale: float

    def set_rotation(self, angle: float):
        self.rotation = angle

    def set_scaling(self, scale: float):
        self.scale = scale

    def set_mirroring(self, mode):
        self.mirroring = mode
