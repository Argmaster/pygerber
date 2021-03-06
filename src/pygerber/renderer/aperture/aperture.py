# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygerber.renderer import Renderer

from pygerber.mathclasses import BoundingBox
from pygerber.renderer.arc_util_mixin import ArcUtilMixin
from pygerber.renderer.spec import ArcSpec, FlashSpec, LineSpec
from pygerber.tokens.add import ADD_Token


class Aperture(ABC, ArcUtilMixin):
    def __init__(self, args: ADD_Token.ARGS, renderer: Renderer) -> None:
        raise TypeError()

    @abstractmethod
    def flash(self, spec: FlashSpec) -> None:
        raise TypeError()

    @abstractmethod
    def line(self, spec: LineSpec) -> None:
        raise TypeError()

    @abstractmethod
    def arc(self, spec: ArcSpec) -> None:
        raise TypeError()

    @abstractmethod
    def bbox(self) -> BoundingBox:
        raise TypeError()

    def flash_bbox(self, spec: FlashSpec) -> BoundingBox:
        return self.bbox().transform(spec.location)

    def line_bbox(self, spec: LineSpec) -> BoundingBox:
        return self.bbox().transform(spec.begin) + self.bbox().transform(spec.end)

    def arc_bbox(self, spec: ArcSpec) -> BoundingBox:
        radius = spec.get_radius() + self.DIAMETER / 2
        return BoundingBox(
            spec.center.x - radius,
            spec.center.y - radius,
            spec.center.x + radius,
            spec.center.y + radius,
        )
