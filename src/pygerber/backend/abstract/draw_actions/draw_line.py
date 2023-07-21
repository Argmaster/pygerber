"""Abstract base class for creating flash draw actions."""
from __future__ import annotations

from abc import ABC, abstractmethod


class DrawLine(ABC):
    """Abstract base class for creating flash drawing actions."""

    @abstractmethod
    def draw(self) -> None:
        """Execute draw action."""
