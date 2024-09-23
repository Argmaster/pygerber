from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

from pygerber.gerberx3.api._gerber_file import GerberFile

if TYPE_CHECKING:
    import PIL.Image


class Project:
    """Multi file project representation.

    This object can be used to render multiple Gerber files to single image.
    It automatically performs alignment and merging of files.
    Files should be ordered bottom up, topmost layer last, like if adding one layer on
    top of previous.
    """

    def __init__(self, files: Iterable[GerberFile]) -> None:
        self.files = list(files)

    def render_with_pillow(self) -> PIL.Image.Image:
        """Render project to raster image using Pillow."""
        raise NotImplementedError
