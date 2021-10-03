# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass

import pygerber.renderer.aperture as meta_ap
from pygerber.mathclasses import Vector2D


class Spec(ABC):
    @abstractmethod
    def draw(self, aperture):
        raise TypeError()

    @abstractmethod
    def bbox(self, aperture):
        raise TypeError()


@dataclass
class FlashSpec(Spec):

    location: Vector2D
    is_region: bool = False

    def draw(self, aperture: meta_ap.Aperture):
        return aperture.flash(self)

    def bbox(self, aperture: meta_ap.Aperture):
        return aperture.flash_bbox(self)


@dataclass
class LineSpec(Spec):

    begin: Vector2D
    end: Vector2D
    is_region: bool = False

    def draw(self, aperture: meta_ap.Aperture):
        return aperture.line(self)

    def bbox(self, aperture: meta_ap.Aperture):
        return aperture.line_bbox(self)


@dataclass
class ArcSpec(Spec):

    begin: Vector2D
    end: Vector2D
    center: Vector2D
    is_region: bool = False

    def draw(self, aperture: meta_ap.Aperture):
        return aperture.arc(self)

    def bbox(self, aperture: meta_ap.Aperture):
        return aperture.arc_bbox(self)

    def get_radius(spec: ArcSpec):
        return (spec.begin - spec.center).length()
