# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygerber.meta.broker import DrawingBroker
from typing import TYPE_CHECKING, List, Tuple

from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec, Spec
from pygerber.tokens.add import ADD_Token

from pygerber.mathclasses import BoundingBox


class Aperture(ABC):
    @abstractmethod
    def __init__(self, args: ADD_Token.ARGS, broker: DrawingBroker) -> None:
        pass

    @abstractmethod
    def flash(self, spec: FlashSpec) -> None:
        pass

    @abstractmethod
    def line(self, spec: LineSpec) -> None:
        pass

    @abstractmethod
    def arc(self, spec: ArcSpec) -> None:
        pass

    @abstractmethod
    def bbox(self) -> BoundingBox:
        pass

    def flash_bbox(self, spec: FlashSpec) -> BoundingBox:
        return self.bbox().transform(spec.location)

    def line_bbox(self, spec: LineSpec) -> BoundingBox:
        return self.bbox().transform(spec.begin) + self.bbox().transform(spec.end)

    def arc_bbox(self, spec: ArcSpec) -> BoundingBox:
        return self.bbox().transform(spec.begin) + self.bbox().transform(spec.end)


class CircularAperture(Aperture):

    DIAMETER: float
    HOLE_DIAMETER: float

    def __init__(self, args: ADD_Token.ARGS, broker: DrawingBroker) -> None:
        self.HOLE_DIAMETER = broker.convert_to_mm(args.HOLE_DIAMETER)
        self.DIAMETER = broker.convert_to_mm(args.DIAMETER)

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

    def __init__(self, args: ADD_Token.ARGS, broker: DrawingBroker) -> None:
        self.X = broker.convert_to_mm(args.X)
        self.Y = broker.convert_to_mm(args.Y)
        self.HOLE_DIAMETER = broker.convert_to_mm(args.HOLE_DIAMETER)

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

    def __init__(self, args: ADD_Token.ARGS, broker: DrawingBroker) -> None:
        super().__init__(args, broker)
        self.VERTICES = args.VERTICES
        self.ROTATION = args.ROTATION


class RegionApertureManager(ABC):
    steps: List[Tuple[Aperture, Spec]]

    @abstractmethod
    def finish(self, bounds: List[Tuple[Aperture, Spec]]) -> None:
        pass

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
