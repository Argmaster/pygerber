"""Abstract base class for creating draw actions."""
from __future__ import annotations

from abc import ABC, abstractmethod

from pygerber.backend.abstract.aperture_handle import PublicApertureHandle
from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.gerberx3.state_enums import Polarity


class DrawAction(ABC):
    """Abstract base class for creating drawing actions."""

    def __init__(
        self,
        handle: PublicApertureHandle,
        backend: Backend,
        polarity: Polarity,
    ) -> None:
        """Initialize DrawAction object."""
        super().__init__()
        self.handle = handle
        self.backend = backend
        self.polarity = polarity
        self.private_handle = self.backend.get_private_aperture_handle(self.handle)

    @abstractmethod
    def draw(self) -> None:
        """Execute draw action."""

    @abstractmethod
    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
