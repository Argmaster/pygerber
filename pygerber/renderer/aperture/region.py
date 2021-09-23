# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple

from pygerber.mathclasses import BoundingBox
from pygerber.renderer.arc_util_mixin import ArcUtilMixin
from pygerber.renderer.spec import Spec
from .aperture import Aperture


class RegionApertureManager(ABC, ArcUtilMixin):
    steps: List[Tuple[Aperture, Spec]]

    def __init__(self, renderer) -> None:
        self.renderer = renderer

    @abstractmethod
    def finish(self, bounds: List[Spec]) -> None:
        raise TypeError()

    def bbox(self, bounds: List[Spec]) -> BoundingBox:
        if len(bounds) == 0:
            return BoundingBox(0, 0, 0, 0)
        spec = bounds[0]
        spec: Spec
        bbox: BoundingBox = BoundingBox(*spec.begin.as_tuple(), *spec.end.as_tuple())
        for spec in bounds[1:]:
            bbox = bbox.include_point(spec.end)
        return bbox
