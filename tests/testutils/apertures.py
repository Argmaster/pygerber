# -*- coding: utf-8 -*-
from pygerber.mathclasses import BoundingBox
from pygerber.meta.apertureset import ApertureSet
from typing import List

from pygerber.meta.aperture import (
    CircularAperture,
    CustomAperture,
    PolygonAperture,
    RectangularAperture,
    RegionApertureManager,
)
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec, Spec


class ApertureCollector:
    class Called(Exception):
        pass

    class CalledWithSpec(Exception):
        def __init__(self, spec: Spec) -> None:
            self.spec = spec

    class CalledFlash(CalledWithSpec):
        pass

    class CalledLine(CalledWithSpec):
        pass

    class CalledArc(CalledWithSpec):
        pass

    class CalledBBox(Called):
        pass

    class CalledFinish(Called):
        def __init__(self, bounds: List[Spec]) -> None:
            self.bounds = bounds

    def flash(self, spec: FlashSpec) -> None:
        raise self.CalledFlash(spec)

    def line(self, spec: LineSpec) -> None:
        raise self.CalledLine(spec)

    def arc(self, spec: ArcSpec) -> None:
        raise self.CalledArc(spec)

    def finish(self, bounds: List[Spec]) -> None:
        raise self.CalledFinish(bounds)


class RectangleApertureCollector(ApertureCollector, RectangularAperture):
    pass


class CircleApertureCollector(ApertureCollector, CircularAperture):
    pass


class PolygonApertureCollector(ApertureCollector, PolygonAperture):
    pass


class RegionApertureCollector(ApertureCollector, RegionApertureManager):
    pass


class CustomApertureCollector(ApertureCollector, CustomAperture):
    def bbox(self):
        return BoundingBox(0, 0, 0, 0)


def get_dummy_apertureSet():
    return ApertureSet(
        CircleApertureCollector,
        RectangleApertureCollector,
        RectangleApertureCollector,
        PolygonApertureCollector,
        CustomApertureCollector,
        RegionApertureCollector,
    )
