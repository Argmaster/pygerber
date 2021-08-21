# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Type

from pygerber.exceptions import NoCorespondingApertureClass
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec, Spec
from pygerber.tokens.add import ADD_Token

from .data import BoundingBox


class Aperture(ABC):
    @abstractmethod
    def __init__(self, args: ADD_Token.ARGS) -> None:
        pass

    @abstractmethod
    def flash(self, spec: FlashSpec) -> None:
        pass

    @abstractmethod
    def line(self) -> None:
        pass

    @abstractmethod
    def arc(self) -> None:
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

    def __init__(self, args: ADD_Token.ARGS) -> None:
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

    def __init__(self, args: ADD_Token.ARGS) -> None:
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

    def __init__(self, args: ADD_Token.ARGS) -> None:
        super().__init__(args)
        self.VERTICES = args.VERTICES
        self.ROTATION = args.ROTATION


class RegionApertureManager(ABC):
    steps: List[Tuple[Aperture, Spec]]

    @abstractmethod
    def finish(self, bounds: List[Tuple[Aperture, Spec]]) -> None:
        pass


@dataclass
class ApertureSet:

    circle: Type[Aperture]
    rectangle: Type[Aperture]
    obround: Type[Aperture]
    polygon: Type[Aperture]
    region: Type[RegionApertureManager]

    def getApertureClass(self, name: str=None, is_region: bool=False) -> Aperture:
        if is_region:
            return self.region
        elif name == "C":
            return self.circle
        elif name == "R":
            return self.rectangle
        elif name == "O":
            return self.obround
        elif name == "P":
            return self.polygon
        else:
            raise NoCorespondingApertureClass(
                f"Missing aperture class for name {name}."
            )


