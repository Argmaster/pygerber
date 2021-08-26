# -*- coding: utf-8 -*-


from pygerber.mathclasses import Vector2D


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

    def __init__(self) -> None:
        self.reset_defaults()

    def reset_defaults(self):
        self.is_regionmode = False
        self.unit = Unit.MILLIMETERS
        self.polarity = Polarity.DARK
        self.interpolation = Interpolation.Linear
        self.current_point = Vector2D(0, 0)

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

    def __init__(self) -> None:
        self.reset_defaults()

    def reset_defaults(self):
        self.mirroring = Mirroring.No
        self.rotation = 0.0
        self.scale = 1.0

    def set_rotation(self, angle: float):
        self.rotation = angle

    def set_scaling(self, scale: float):
        self.scale = scale

    def set_mirroring(self, mode):
        self.mirroring = mode
