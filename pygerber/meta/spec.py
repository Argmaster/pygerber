# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List

from pygerber.mathclasses import Vector2D


class Spec:
    pass


@dataclass
class FlashSpec(Spec):

    location: Vector2D
    is_region: bool


@dataclass
class LineSpec(Spec):

    begin: Vector2D
    end: Vector2D
    is_region: bool


@dataclass
class ArcSpec(Spec):

    begin: Vector2D
    end: Vector2D
    center: Vector2D
    is_region: bool


@dataclass
class RegionSpec(Spec):

    bounds: List[Spec]
