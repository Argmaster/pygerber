# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Deque
from typing import List
from typing import Tuple

from pygerber.constants import Interpolation
from pygerber.drawing_state import DrawingState
from pygerber.exceptions import EndOfStream
from pygerber.mathclasses import BoundingBox
from pygerber.mathclasses import Vector2D
from pygerber.tokens.token import Token

from .aperture import RegionApertureManager
from .aperture_manager import ApertureManager
from .apertureset import ApertureSet
from .spec import ArcSpec
from .spec import FlashSpec
from .spec import LineSpec
from .spec import Spec


class Renderer:

    current_point: Vector2D
    region_bounds: List[Spec]

    apertures: ApertureManager
    state: DrawingState

    def __init__(self, apertureSet: ApertureSet) -> None:
        self.apertures = ApertureManager(apertureSet, self)
        self.state = DrawingState()
        self.set_defaults()

    def set_defaults(self):
        self.apertures.set_defaults()
        self.state.set_defaults()
        self.current_point = Vector2D(0, 0)
        self.region_bounds = []

    def render(self, token_stack: Deque[Token]) -> None:
        try:
            for token in token_stack:
                token.alter_state(self.state)
                token.pre_render(self)
                token.render(self)
                token.post_render(self)
        except EndOfStream:
            return

    def define_aperture(self, *args, **kwargs):
        self.apertures.define_aperture(*args, **kwargs)

    def select_aperture(self, id: int):
        self.apertures.select_aperture(id)

    def total_bounding_box(self, token_stack: Deque[Token]):
        total_bbox: BoundingBox = None
        try:
            for token in token_stack:
                total_bbox = self.__update_bounding_box(token, total_bbox)
        except EndOfStream:
            pass
        self.set_defaults()
        if total_bbox is None:
            return BoundingBox(0, 0, 0, 0)
        else:
            return total_bbox

    def __update_bounding_box(self, token, total_bbox):
        token.alter_state(self.state)
        token.pre_render(self)
        bbox = token.bbox(self)
        if bbox is not None:
            if total_bbox is None:
                total_bbox = bbox
            else:
                total_bbox = total_bbox + bbox
        token.post_render(self)
        return total_bbox

    def draw_interpolated(self, end: Vector2D, offset: Vector2D) -> None:
        if self.state.interpolation == Interpolation.Linear:
            self.draw_line(end)
        else:
            self.draw_arc(end, offset)

    def bbox_interpolated(self, end: Vector2D, offset: Vector2D) -> BoundingBox:
        if self.state.interpolation == Interpolation.Linear:
            return self.bbox_line(end)
        else:
            return self.bbox_arc(end, offset)

    def draw_line(self, end: Vector2D) -> None:
        spec = self.__get_line_spec(end)
        if self.state.is_regionmode:
            self.__push_region_step(spec)
        else:
            self.apertures.get_current_aperture().line(spec)

    def bbox_line(self, end: Vector2D) -> None:
        spec = self.__get_line_spec(end)
        if self.state.is_regionmode:
            self.__push_region_step(spec)
        else:
            return self.apertures.get_current_aperture().line_bbox(spec)

    def __get_line_spec(self, end: Vector2D) -> LineSpec:
        return LineSpec(
            self.current_point,
            self.replace_none_with_current(end),
            self.state.is_regionmode,
        )

    def draw_arc(self, end: Vector2D, offset: Vector2D) -> None:
        spec = self.__get_arc_spec(end, offset)
        if self.state.is_regionmode:
            self.__push_region_step(spec)
        else:
            self.apertures.get_current_aperture().arc(spec)

    def bbox_arc(self, end: Vector2D, offset: Vector2D) -> None:
        spec = self.__get_arc_spec(end, offset)
        if self.state.is_regionmode:
            self.__push_region_step(spec)
        else:
            return self.apertures.get_current_aperture().arc_bbox(spec)

    def __get_arc_spec(self, end: Vector2D, offset: Vector2D) -> ArcSpec:
        return ArcSpec(
            self.current_point,
            self.replace_none_with_current(end),
            self.current_point + self.replace_none_with_0(offset),
            self.state.is_regionmode,
        )

    def draw_flash(self, point: Vector2D) -> None:
        if self.state.is_regionmode:
            raise RuntimeError("Flashes can't be used in region mode.")
        else:
            aperture = self.apertures.get_current_aperture()
            spec = self.__get_flash_spec(point)
            aperture.flash(spec)

    def bbox_flash(self, point: Vector2D) -> BoundingBox:
        self.move_pointer(point)
        aperture = self.apertures.get_current_aperture()
        spec = self.__get_flash_spec(point)
        return aperture.flash_bbox(spec)

    def __get_flash_spec(self, point: Vector2D) -> FlashSpec:
        spec = FlashSpec(
            self.replace_none_with_current(point),
            self.state.is_regionmode,
        )
        return spec

    def __push_region_step(self, spec: Spec):
        self.region_bounds.append(spec)
        self.move_pointer(spec.end)

    def end_region(self):
        self.state.end_region()

    def finish_drawing_region(self) -> Tuple[RegionApertureManager, List[Spec]]:
        bounds = self.__get_and_clean_region_bounds()
        apertureClass = self.apertures.getApertureClass(None, True)
        return apertureClass(self), bounds

    def __get_and_clean_region_bounds(self):
        bounds = self.region_bounds
        self.region_bounds = []
        return bounds

    def move_pointer(self, location: Vector2D) -> None:
        self.current_point = Vector2D(
            location.x if location.x is not None else self.current_point.x,
            location.y if location.y is not None else self.current_point.y,
        )

    def isCCW(self):
        return self.state.interpolation == Interpolation.CounterclockwiseCircular

    def replace_none_with_current(self, vector: Vector2D):
        if vector.x is None:
            vector.x = self.current_point.x
        if vector.y is None:
            vector.y = self.current_point.y
        return vector

    def replace_none_with_0(self, vector: Vector2D):
        if vector.x is None:
            vector.x = 0
        if vector.y is None:
            vector.y = 0
        return vector
