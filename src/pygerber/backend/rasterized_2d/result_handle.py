"""Module contains handle class to drawing instructions visualization."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from PIL import Image

from pygerber.backend.abstract.result_handle import ResultHandle

if TYPE_CHECKING:
    from io import BytesIO


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

    def save(
        self,
        dest: Path | str | BytesIO,
        **kwargs: Any,
    ) -> None:
        """Save result to destination.

        Parameters
        ----------
        dest : Path | str | BytesIO
            Write target.
        **kwargs: Any
            Extra parameters which will be passed to `Image.save()`.
            For details see [Pillow documentation](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save).

        """
        image = self.get_image()
        if (isinstance(dest, Path) and dest.suffix in (".jpg", "jpeg")) or (
            isinstance(dest, str) and (dest.endswith((".jpg", ".jpeg")))
        ):
            image = image.convert("RGB")
        image.save(dest, **kwargs)

    def get_image(self) -> Image.Image:
        """Get result image object."""
        return self.result.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
