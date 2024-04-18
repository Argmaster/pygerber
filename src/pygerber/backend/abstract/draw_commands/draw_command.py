"""Base class for creating components for aperture creation."""

from __future__ import annotations

from abc import ABC, abstractmethod

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.drawing_target import DrawingTarget
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.state_enums import Polarity


class DrawCommand(ABC):
    """Description of aperture component."""

    backend: Backend
    polarity: Polarity

    def __init__(self, backend: Backend, polarity: Polarity) -> None:
        """Initialize draw command."""
        self.backend = backend
        self.polarity = polarity

    @abstractmethod
    def draw(self, target: DrawingTarget) -> None:
        """Apply aperture draw component to handle."""

    @abstractmethod
    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}({self.polarity})"
