"""Abstract base class for creating arc draw actions."""
from __future__ import annotations

from pygerber.backend.abstract.aperture_handle import PublicApertureHandle
from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.backend.abstract.draw_actions.draw_action import DrawAction
from pygerber.backend.abstract.offset import Offset
from pygerber.backend.abstract.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity


class DrawArc(DrawAction):
    """Abstract base class for creating arc drawing actions."""

    def __init__(  # noqa: PLR0913
        self,
        handle: PublicApertureHandle,
        backend: Backend,
        polarity: Polarity,
        start_position: Vector2D,
        dx_dy_center: Vector2D,
        end_position: Vector2D,
    ) -> None:
        """Initialize DrawFlash object."""
        super().__init__(handle, backend, polarity)
        self.start_position = start_position
        self.dx_dy_center = dx_dy_center
        self.end_position = end_position

    @property
    def arc_center_absolute(self) -> Vector2D:
        """Return absolute coordinates of arc center point."""
        return self.start_position + self.dx_dy_center

    @property
    def arc_space_arc_center(self) -> Vector2D:
        """Return arc center coordinates relative to arc center."""
        return self.arc_center_absolute - self.arc_center_absolute

    @property
    def arc_space_start_position(self) -> Vector2D:
        """Return arc start coordinates relative to arc center."""
        return self.start_position - self.arc_center_absolute

    @property
    def arc_space_end_position(self) -> Vector2D:
        """Return arc end coordinates relative to arc center."""
        return self.end_position - self.arc_center_absolute

    @property
    def arc_radius(self) -> Offset:
        """Return arc radius."""
        return self.dx_dy_center.length()

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        aperture_bbox = self.private_handle.get_bounding_box()
        radius = self.arc_radius
        return (aperture_bbox + self.arc_center_absolute + radius) + (
            aperture_bbox + self.arc_center_absolute - radius
        )
