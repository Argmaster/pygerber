"""Abstract base class for creating arc draw actions."""
from __future__ import annotations

from abc import ABC, abstractmethod


class DrawArc(ABC):
    """Abstract base class for creating arc drawing actions."""

    @abstractmethod
    def draw(self) -> None:
        """Execute draw action."""
