"""Abstract base class for creating flash draw actions."""
from __future__ import annotations

from pygerber.backend.abstract.aperture_handle import PublicApertureHandle
from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.backend.abstract.draw_actions.draw_action import DrawAction
from pygerber.backend.abstract.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity


class DrawFlash(DrawAction):
    """Abstract base class for creating flash drawing actions."""

    def __init__(
        self,
        handle: PublicApertureHandle,
        backend: Backend,
        polarity: Polarity,
        position: Vector2D,
    ) -> None:
        """Initialize DrawFlash object."""
        super().__init__(handle, backend, polarity)
        self.position = position

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        return self.private_handle.get_bounding_box() + self.position
