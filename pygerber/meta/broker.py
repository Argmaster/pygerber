# -*- coding: utf-8 -*-
from pygerber.exceptions import ApertureSelectionError
from typing import List, Tuple

from .aperture import Aperture, ApertureSet
from .aperture_manager import ApertureManager
from .data import Vector2D
from .meta import DrawingMeta, TransformMeta
from .spec import ArcSpec, FlashSpec, LineSpec, Spec


class DrawingBroker(ApertureManager, TransformMeta, DrawingMeta):
    current_aperture: Aperture
    current_point: Vector2D
    region_bounds: List[Tuple[Aperture, Spec]]

    def __init__(self, apertureSet: ApertureSet) -> None:
        self.current_aperture = None
        self.current_point = Vector2D(0, 0)
        self.region_bounds = []
        ApertureManager.__init__(self, apertureSet)
        TransformMeta.__init__(self)
        DrawingMeta.__init__(self)

    def select_aperture(self, id: int):
        self.current_aperture = self.get_aperture(id)

    def draw_line(self, end: Vector2D) -> None:
        spec = LineSpec(
            self.current_point,
            end,
            self.is_regionmode,
        )
        if self.is_regionmode:
            self.push_region_step(spec)
        else:
            self.get_current_aperture().line(spec)

    def draw_arc(self, end: Vector2D, offset: Vector2D) -> None:
        spec = ArcSpec(
            self.current_point,
            end,
            # TODO Not entirely sure how center should be calculated
            self.current_point + offset,
            self.is_regionmode,
        )
        if self.is_regionmode:
            self.push_region_step(spec)
        else:
            self.get_current_aperture().arc(spec)

    def draw_flash(self, point: Vector2D) -> None:
        spec = FlashSpec(
            point,
            self.is_regionmode,
        )
        if self.is_regionmode:
            raise RuntimeError("Flashes can't be used in region mode.")
        else:
            self.get_current_aperture().flash(spec)

    def draw_interpolated(self, end: Vector2D, offset: Vector2D) -> None:
        if self.interpolation == DrawingMeta.Interpolation.Linear:
            self.draw_line(end)
        else:
            self.draw_arc(end, offset)

    def get_current_aperture(self):
        if self.current_aperture is None:
            raise ApertureSelectionError(
                "Attempt to perform operation with aperture without preceding aperture selection."
            )
        return self.current_aperture

    def end_region(self):
        apertureClass = self.apertureSet.getApertureClass(None, True)
        bounds = self.region_bounds
        self.region_bounds = []
        super().end_region()
        apertureClass().finish(bounds)

    def move_pointer(self, location: Vector2D) -> None:
        self.current_point = self.fill_xy_none_with_current(location)

    def fill_xy_none_with_current(self, point: Vector2D):
        if point.x is None:
            point.x = self.current_point.x
        if point.y is None:
            point.y = self.current_point.y
        return point

    def push_region_step(self, spec: Spec):
        self.region_bounds.append((self.current_aperture, spec))
