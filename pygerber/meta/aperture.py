# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Tuple, Type

from pygerber.exceptions import ApertureSelectionError, NoCorespondingApertureClass
from pygerber.meta.spec import Spec
from pygerber.tokens.add import ADD_Token

from .data import BoundingBox


class Aperture(ABC):
    def __init__(
        self, args: ADD_Token.ARGS, *, STEPS: List[Tuple[Aperture, Spec]] = None
    ) -> None:
        pass

    @abstractmethod
    def flash(self) -> None:
        pass

    @abstractmethod
    def line(self) -> None:
        pass

    @abstractmethod
    def arc(self) -> None:
        pass

    def region(self) -> None:
        pass

    @abstractmethod
    def bbox(self) -> BoundingBox:
        pass


class CircularAperture(Aperture):

    DIAMETER: float
    HOLE_DIAMETER: float

    def __init__(
        self, args: ADD_Token.ARGS, *, _: List[Tuple[Aperture, Spec]] = None
    ) -> None:
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

    def __init__(
        self, args: ADD_Token.ARGS, *, _: List[Tuple[Aperture, Spec]] = None
    ) -> None:
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

    def __init__(
        self, args: ADD_Token.ARGS, *, _: List[Tuple[Aperture, Spec]] = None
    ) -> None:
        super().__init__(args)
        self.VERTICES = args.VERTICES
        self.ROTATION = args.ROTATION


class RegionAperture(Aperture):

    STEPS: float

    def __init__(
        self, _: ADD_Token.ARGS, *, STEPS: List[Tuple[Aperture, Spec]]
    ) -> None:
        self.STEPS = STEPS


@dataclass
class ApertureSet:

    circle: Type[Aperture]
    rectangle: Type[Aperture]
    obround: Type[Aperture]
    polygon: Type[Aperture]
    region: Type[Aperture]

    def getApertureClass(self, name: str, is_region: bool) -> Aperture:
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


class ApertureManager:
    apertures: Dict[int, Aperture]
    apertureSet: ApertureSet
    region_bounds: List[Tuple[Aperture, Spec]]

    def bindApertureSet(self, apSet: ApertureSet):
        self.apertureSet = apSet

    def defineAperture(self, token: ADD_Token):
        if token.TYPE is not None:
            apertureClass = self.apertureSet.getApertureClass(token.TYPE)
        else:
            apertureClass = self.apertureSet.getApertureClass(token.NAME)
        self.apertures[token.ID] = apertureClass(token.ARGS)

    def selectAperture(self, id: int):
        new_aperture = self.apertures.get(id, None)
        if new_aperture is None:
            raise ApertureSelectionError(f"Aperture with ID {id} was not defined.")
        else:
            self.current_aperture = new_aperture

    def pushRegionStep(self, spec: Spec):
        self.region_bounds.append((self.current_aperture, spec))
