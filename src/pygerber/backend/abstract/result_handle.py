"""Module contains handle class to drawing instructions visualization."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from io import BytesIO
    from pathlib import Path


class ResultHandle(ABC):
    """Handle to drawing instructions visualization."""

    @abstractmethod
    def save(self, dest: Path | str | BytesIO) -> None:
        """Save result to destination."""
