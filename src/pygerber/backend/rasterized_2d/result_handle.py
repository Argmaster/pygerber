"""Module contains handle class to drawing instructions visualization."""
from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.backend.abstract.result_handle import ResultHandle

if TYPE_CHECKING:
    from io import BytesIO
    from pathlib import Path


class Rasterized2DResultHandle(ResultHandle):
    """Handle to drawing instructions visualization."""

    def save(self, dest: Path | str | BytesIO) -> None:
        """Save result to destination."""
