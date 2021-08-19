# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC
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

    def flash(self) -> None:
        pass

    def line(self) -> None:
        pass

    def arc(self) -> None:
        pass

    def region(self) -> None:
        pass

    def bbox(self) -> BoundingBox:
        pass


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
