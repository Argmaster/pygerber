# -*- coding: utf-8 -*-
from typing import List, Tuple

from pygerber.exceptions import ApertureSelectionError
from pygerber.mathclasses import BoundingBox, Vector2D

from .aperture import Aperture, RegionApertureManager
from .aperture_manager import ApertureManager
from .apertureset import ApertureSet
from .meta import Interpolation, TransformMeta
from .spec import ArcSpec, FlashSpec, LineSpec, Spec


class DrawingBroker(ApertureManager, TransformMeta):
    current_aperture: Aperture
    current_point: Vector2D
    region_bounds: List[Spec]

    def __init__(self, apertureSet: ApertureSet) -> None:
        self.reset_defaults()
        ApertureManager.__init__(self, apertureSet)
        TransformMeta.__init__(self)

    def reset_defaults(self):
        ApertureManager.reset_defaults(self)
        TransformMeta.reset_defaults(self)
        self.current_aperture = None
        self.current_point = Vector2D(0, 0)
        self.region_bounds = []

    def select_aperture(self, id: int):
        self.current_aperture = self.get_aperture(id)

    def draw_interpolated(self, end: Vector2D, offset: Vector2D) -> None:
        if self.interpolation == Interpolation.Linear:
            self.draw_line(end)
        else:
            self.draw_arc(end, offset)

    def bbox_interpolated(self, end: Vector2D, offset: Vector2D) -> BoundingBox:
        if self.interpolation == Interpolation.Linear:
            return self.bbox_line(end)
        else:
            return self.bbox_arc(end, offset)

    def draw_line(self, end: Vector2D) -> None:
        spec = self._get_line_spec(end)
        if self.is_regionmode:
            self._push_region_step(spec)
        else:
            self.get_current_aperture().line(spec)

    def bbox_line(self, end: Vector2D) -> None:
        spec = self._get_line_spec(end)
        if self.is_regionmode:
            self._push_region_step(spec)
        else:
            return self.get_current_aperture().line_bbox(spec)

    def _get_line_spec(self, end: Vector2D) -> LineSpec:
        return LineSpec(
            self.current_point,
            end,
            self.is_regionmode,
        )

    def draw_arc(self, end: Vector2D, offset: Vector2D) -> None:
        spec = self._get_arc_spec(end, offset)
        if self.is_regionmode:
            self._push_region_step(spec)
        else:
            self.get_current_aperture().arc(spec)

    def bbox_arc(self, end: Vector2D, offset: Vector2D) -> None:
        spec = self._get_arc_spec(end, offset)
        if self.is_regionmode:
            self._push_region_step(spec)
        else:
            return self.get_current_aperture().arc_bbox(spec)

    def _get_arc_spec(self, end: Vector2D, offset: Vector2D) -> ArcSpec:
        return ArcSpec(
            self.current_point,
            end,
            # TODO Not entirely sure how center should be calculated
            self.current_point + offset,
            self.is_regionmode,
        )

    def draw_flash(self, point: Vector2D) -> None:
        if self.is_regionmode:
            raise RuntimeError("Flashes can't be used in region mode.")
        else:
            self.move_pointer(point)
            aperture = self.get_current_aperture()
            spec = self._get_flash_spec(point)
            aperture.flash(spec)

    def bbox_flash(self, point: Vector2D) -> BoundingBox:
        self.move_pointer(point)
        aperture = self.get_current_aperture()
        spec = self._get_flash_spec(point)
        return aperture.flash_bbox(spec)

    def _get_flash_spec(self, point: Vector2D) -> FlashSpec:
        spec = FlashSpec(
            point,
            self.is_regionmode,
        )
        return spec

    def get_current_aperture(self):
        if self.current_aperture is None:
            raise ApertureSelectionError(
                "Attempt to perform operation with aperture without preceding aperture selection."
            )
        return self.current_aperture

    def end_region(self) -> Tuple[RegionApertureManager, List[Spec]]:
        bounds = self._get_and_clean_region_bounds()
        super().end_region()
        apertureClass = self.apertureSet.getApertureClass(None, True)
        return apertureClass, bounds

    def _get_and_clean_region_bounds(self):
        bounds = self.region_bounds
        self.region_bounds = []
        return bounds

    def move_pointer(self, location: Vector2D) -> None:
        self.current_point = location

    def _push_region_step(self, spec: Spec):
        self.region_bounds.append(spec)

    def isCCW(self):
        return self.interpolation == Interpolation.CounterclockwiseCircular
