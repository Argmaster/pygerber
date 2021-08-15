from unittest.result import TestResult
from pygerber.coparser import CoParser
from typing import Tuple


class Meta:
    class Unit:
        MILIMETERS = "MM"
        INCHES = "IN"

    class Polarity:
        DARK = "D"
        CLEAR = "C"

    class Interpolation:
        Linear = "G01"
        ClockwiseCircular = "G02"
        CounterclockwiseCircular = "G03"
        _BeforeCircular = "G75"

    class Mirroring:
        No = "N"
        X = "X"
        Y = "Y"
        XY = "XY"

    def __init__(
        self,
        ignore_deprecated: bool=True,
        coparser: CoParser=None,
        unit: Unit=Unit.MILIMETERS,
        current_point: Tuple[float, float] = (0,0),
        current_aperture: object = None,
        interpolation: Interpolation = Interpolation.Linear,
        polarity: Polarity = Polarity.DARK,
        mirroring: Mirroring = Mirroring.No,
        rotation: float = 0,
        scaling: float = 0,
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
        self.polarity = polarity
        self.mirroring = mirroring
        self.rotation = rotation
        self.scaling = scaling
