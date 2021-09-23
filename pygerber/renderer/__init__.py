# class Meta(DrawingBroker):
#
#     coparser = CoParser
#
#     def __init__(
#         self,
#         apertureSet: ApertureSet,
#         *,
#         ignore_deprecated: bool = True,
#     ) -> None:
#         super().__init__(apertureSet)
#         self.ignore_deprecated = ignore_deprecated
#         self.coparser = CoParser()
#
#     def set_defaults(self):
#         super().set_defaults()
#
#     def raiseDeprecatedSyntax(self, message: str):
#         if not self.ignore_deprecated:
#             raise DeprecatedSyntax(message)
# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.renderer.aperture.aperture import Aperture
from pygerber.exceptions import EndOfStream
from typing import List, Tuple

from pygerber.mathclasses import BoundingBox, Vector2D

from .aperture import RegionApertureManager
from .aperture_manager import ApertureManager
from .apertureset import ApertureSet
from .spec import ArcSpec, FlashSpec, LineSpec, Spec
from pygerber.drawing_state import DrawingState, Interpolation
from pygerber.tokens.token import Token


class Renderer:

    current_point: Vector2D
    region_bounds: List[Spec]

    apertures: ApertureManager
    state: DrawingState

    def __init__(self, apertureSet: ApertureSet) -> None:
        self.apertures = ApertureManager(apertureSet)
        self.state = DrawingState()
        self.set_defaults()

    def render(self) -> None:
        """
        Render all tokens contained in token_stack.
        """
        try:
            for token in self.token_stack:
                self.__render_token(token)
        except EndOfStream:
            return

    def __render_token(self, token: Token) -> None:
        token: Token
        token.alter_state()
        token.pre_render()
        token.render()
        token.post_render()

    def set_defaults(self):
        self.apertures.set_defaults()
        self.state.set_defaults()
        self.current_point = Vector2D(0, 0)
        self.region_bounds = []

    def define_aperture(self, *args, **kwargs):
        self.apertures.define_aperture(*args, **kwargs)

    def select_aperture(self, id: int):
        self.apertures.select_aperture(id)

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

    def __push_region_step(self, spec: Spec):
        self.region_bounds.append(spec)

    def bbox_line(self, end: Vector2D) -> None:
        spec = self.__get_line_spec(end)
        if self.state.is_regionmode:
            self.__push_region_step(spec)
        else:
            return self.apertures.get_current_aperture().line_bbox(spec)

    def __get_line_spec(self, end: Vector2D) -> LineSpec:
        return LineSpec(
            self.current_point,
            end,
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
            end,
            # TODO Not entirely sure how center should be calculated
            self.current_point + offset,
            self.state.is_regionmode,
        )

    def draw_flash(self, point: Vector2D) -> None:
        if self.state.is_regionmode:
            raise RuntimeError("Flashes can't be used in region mode.")
        else:
            self.move_pointer(point)
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
            point,
            self.state.is_regionmode,
        )
        return spec

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
        self.current_point = location

    def isCCW(self):
        return self.state.interpolation == Interpolation.CounterclockwiseCircular
