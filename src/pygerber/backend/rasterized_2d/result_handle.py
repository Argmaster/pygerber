"""Module contains handle class to drawing instructions visualization."""
from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image

from pygerber.backend.abstract.result_handle import ResultHandle

if TYPE_CHECKING:
    from io import BytesIO
    from pathlib import Path


class Rasterized2DResultHandle(ResultHandle):
    """Handle to drawing instructions visualization."""

    def __init__(self, result: Image.Image) -> None:
        """Initialize result handle.

        Parameters
        ----------
        result : Image.Image
            Image object containing finished Gerber image.
        """
        super().__init__()
        self.result = result

    def save(self, dest: Path | str | BytesIO) -> None:
        """Save result to destination."""
        self.result.transpose(Image.FLIP_TOP_BOTTOM).save(dest)
