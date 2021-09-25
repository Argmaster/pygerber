# -*- coding: utf-8 -*-
from __future__ import annotations


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
