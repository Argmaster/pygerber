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
        self.is_regionmode = False
        self.unit = Unit.MILLIMETERS
        self.polarity = Polarity.DARK
        self.interpolation = Interpolation.Linear

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

    def preprocess_vector(self, vector: Vector2D) -> Vector2D:
        return self.fill_xy_none_with_current(self.convert_vector_to_mm(vector))

    def preprocess_offset(self, vector: Vector2D) -> Vector2D:
        return self.fill_xy_none_with_zero(self.convert_vector_to_mm(vector))

    def fill_xy_none_with_current(self, point: Vector2D):
        if point.x is None:
            point.x = self.current_point.x
        if point.y is None:
            point.y = self.current_point.y
        return point

    def fill_xy_none_with_zero(self, point: Vector2D):
        if point.x is None:
            point.x = 0
        if point.y is None:
            point.y = 0
        return point

    def convert_to_mm(self, value: float):
        if self.unit == Unit.INCHES:
            return value * 25.4
        else:
            return value

    def convert_vector_to_mm(self, vector: Vector2D):
        return Vector2D(
            self.convert_to_mm(vector.x),
            self.convert_to_mm(vector.y),
        )

class TransformMeta:

    mirroring: str
    rotation: float
    scale: float

    def __init__(self) -> None:
        self.mirroring = Mirroring.No
        self.rotation = 0.0
        self.scale = 1.0

    def set_rotation(self, angle: float):
        self.rotation = angle

    def set_scaling(self, scale: float):
        self.scale = scale

    def set_mirroring(self, mode):
        self.mirroring = mode
