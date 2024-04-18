"""Module contains handle class to drawing instructions visualization."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from io import BytesIO
    from pathlib import Path


class ResultHandle(ABC):
    """Handle to drawing instructions visualization."""

    @abstractmethod
    def save(
        self,
        dest: Path | str | BytesIO,
        **kwargs: Any,
    ) -> None:
        """Save result to destination.

        All additional parameters are passed to underlying saving system.
        For more details see documentation of concrete implementations.
        """
