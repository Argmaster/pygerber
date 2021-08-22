# -*- coding: utf-8 -*-
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from pygerber.meta.aperture import Aperture

from pygerber.mathclasses import Vector2D


class Spec(ABC):

    @abstractmethod
    def draw(self, aperture):
        pass

    @abstractmethod
    def bbox(self, aperture):
        pass


@dataclass
class FlashSpec(Spec):

    location: Vector2D
    is_region: bool

    def draw(self, aperture: Aperture):
        return aperture.flash(self)

    def bbox(self, aperture: Aperture):
        return aperture.flash_bbox(self)

@dataclass
class LineSpec(Spec):

    begin: Vector2D
    end: Vector2D
    is_region: bool

    def draw(self, aperture: Aperture):
        return aperture.line(self)

    def bbox(self, aperture: Aperture):
        return aperture.line_bbox(self)


@dataclass
class ArcSpec(Spec):

    begin: Vector2D
    end: Vector2D
    center: Vector2D
    is_region: bool

    def draw(self, aperture: Aperture):
        return aperture.arc(self)

    def bbox(self, aperture: Aperture):
        return aperture.arc_bbox(self)

