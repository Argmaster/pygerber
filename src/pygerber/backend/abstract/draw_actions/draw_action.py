"""Abstract base class for creating draw actions."""
from __future__ import annotations

from abc import ABC, abstractmethod

from pygerber.backend.abstract.bounding_box import BoundingBox


class DrawAction(ABC):
    """Abstract base class for creating drawing actions."""

    @abstractmethod
    def draw(self) -> None:
        """Execute draw action."""

    @abstractmethod
    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
