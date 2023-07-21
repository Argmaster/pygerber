"""Abstract base class for creating draw actions."""
from __future__ import annotations

from abc import ABC, abstractmethod


class DrawAction(ABC):
    """Abstract base class for creating drawing actions."""

    @abstractmethod
    def draw(self) -> None:
        """Execute draw action."""
