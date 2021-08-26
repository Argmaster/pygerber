# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Type

from .aperture import Aperture, RegionApertureManager


@dataclass
class ApertureSet:

    circle: Type[Aperture]
    rectangle: Type[Aperture]
    obround: Type[Aperture]
    polygon: Type[Aperture]
    custom: Type[Aperture]
    region: Type[RegionApertureManager]

    def getApertureClass(self, name: str = None, is_region: bool = False) -> Aperture:
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
            return self.custom
