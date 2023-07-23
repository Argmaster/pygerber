"""Abstract base class for creating line draw actions."""
from __future__ import annotations

from pygerber.backend.abstract.aperture_handle import PublicApertureHandle
from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.backend.abstract.draw_actions.draw_action import DrawAction
from pygerber.backend.abstract.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity


class DrawLine(DrawAction):
    """Abstract base class for creating line drawing actions."""

    def __init__(  # noqa: PLR0913
        self,
        handle: PublicApertureHandle,
        backend: Backend,
        polarity: Polarity,
        start_position: Vector2D,
        end_position: Vector2D,
    ) -> None:
        """Initialize DrawFlash object."""
        super().__init__(handle, backend, polarity)
        self.start_position = start_position
        self.end_position = end_position

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        aperture_bbox = self.private_handle.get_bounding_box()
        return (aperture_bbox + self.start_position) + (
            aperture_bbox + self.end_position
        )
