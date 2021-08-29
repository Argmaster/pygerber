# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC, abstractmethod
from pygerber.meta.arc_util_mixin import ArcUtilMixin

from typing import List, Tuple

from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec, Spec
from pygerber.tokens.add import ADD_Token

from pygerber.mathclasses import BoundingBox


class Aperture(ABC, ArcUtilMixin):

    def __init__(self, args: ADD_Token.ARGS, broker) -> None:
        raise TypeError()

    @abstractmethod
    def flash(self, spec: FlashSpec) -> None:
        raise TypeError()

    @abstractmethod
    def line(self, spec: LineSpec) -> None:
        raise TypeError()

    @abstractmethod
    def arc(self, spec: ArcSpec) -> None:
        raise TypeError()

    @abstractmethod
    def bbox(self) -> BoundingBox:
        raise TypeError()

    def flash_bbox(self, spec: FlashSpec) -> BoundingBox:
        return self.bbox().transform(spec.location)

    def line_bbox(self, spec: LineSpec) -> BoundingBox:
        return self.bbox().transform(spec.begin) + self.bbox().transform(spec.end)

    def arc_bbox(self, spec: ArcSpec) -> BoundingBox:
        radius = spec.get_radius() + self.DIAMETER / 2
        return BoundingBox(
            spec.center.x - radius,
            spec.center.y - radius,
            spec.center.x + radius,
            spec.center.y + radius,
        )

class CircularAperture(Aperture):

    DIAMETER: float
    HOLE_DIAMETER: float

    def __init__(self, args: ADD_Token.ARGS, broker) -> None:
        self.broker = broker
        self.HOLE_DIAMETER = args.HOLE_DIAMETER
        self.DIAMETER = args.DIAMETER

    def bbox(self) -> BoundingBox:
        d_half = self.DIAMETER / 2
        return BoundingBox(
            -d_half,
            d_half,
            d_half,
            -d_half,
        )


class RectangularAperture(Aperture):

    X: float
    Y: float
    HOLE_DIAMETER: float

    def __init__(self, args: ADD_Token.ARGS, broker) -> None:
        self.broker = broker
        self.X = args.X
        self.Y = args.Y
        self.HOLE_DIAMETER = args.HOLE_DIAMETER

    def bbox(self) -> BoundingBox:
        x_half = self.X / 2
        y_half = self.Y / 2
        return BoundingBox(
            -x_half,
            y_half,
            x_half,
            -y_half,
        )


class PolygonAperture(CircularAperture):

    VERTICES: float
    ROTATION: float
    DIAMETER: float
    HOLE_DIAMETER: float

    def __init__(self, args: ADD_Token.ARGS, broker) -> None:
        super().__init__(args, broker)
        self.VERTICES = args.VERTICES
        self.ROTATION = args.ROTATION


class RegionApertureManager(ABC, ArcUtilMixin):
    steps: List[Tuple[Aperture, Spec]]

    def __init__(self, broker) -> None:
        self.broker = broker

    @abstractmethod
    def finish(self, bounds: List[Tuple[Aperture, Spec]]) -> None:
        raise TypeError()

    def bbox(self, bounds: List[Tuple[Aperture, Spec]]) -> BoundingBox:
        if len(bounds) == 0:
            return BoundingBox(0, 0, 0, 0)
        aperture, spec = bounds[0]
        aperture: Aperture
        spec: Spec
        bbox = spec.bbox(aperture)
        for bound in bounds[1:]:
            aperture, spec = bound
            bbox = bbox + spec.bbox(aperture)
        return bbox


class CustomAperture(Aperture):

    def __init__(self, args: ADD_Token.ARGS, broker) -> None:
        self.broker = broker
        self.args = args
        self.process_args()

    def process_args(self):
        pass