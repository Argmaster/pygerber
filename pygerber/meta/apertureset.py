# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Type

from pygerber.exceptions import NoCorespondingApertureClass

from .aperture import Aperture, RegionApertureManager


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
