from __future__ import annotations

from typing import Iterable, Sequence

from PIL import Image

from pygerber.gerber.api._gerber_file import GerberFile, PillowImage


class CompositeImage:
    """Image composed of multiple sub-images."""


class CompositePillowImage(CompositeImage):
    """Image composed of multiple sub-images."""

    def __init__(self, sub_images: list[PillowImage], image: Image.Image) -> None:
        self._sub_images = sub_images
        self._image = image

    def get_sub_images(self) -> Sequence[PillowImage]:
        """Get sequence containing sub-images."""
        return self._sub_images

    def get_image(self) -> Image.Image:
        """Get image composed out of sub-images."""
        return self._image


class CompositeView:
    """View composed of multiple Gerber files.

    Composite view is a generalized concept of a top / bottom / inner layer view
    extracted from a Gerber project. Usually it does not make sense to render all
    layers at once, as bottom layers will be simply covered by top layers.

    This object can be used to render selected Gerber files to single image.
    It automatically performs alignment and merging of files.
    Files should be ordered bottom up, topmost layer last, like if adding one layer on
    top of previous.
    """

    def __init__(self, files: Iterable[GerberFile]) -> None:
        self._files = tuple(files)

    @property
    def files(self) -> tuple[GerberFile, ...]:
        """Get sequence of Gerber files."""
        return self._files

    def render_with_pillow(
        self,
        dpmm: int = 20,
    ) -> CompositePillowImage:
        """Render project to raster image using Pillow."""
        sub_images: list[PillowImage] = [
            file.render_with_pillow(dpmm=dpmm) for file in self.files
        ]

        max_x_image = max(sub_images, key=lambda x: x.get_image_space().max_x)
        max_y_image = max(sub_images, key=lambda x: x.get_image_space().max_y)
        min_x_image = min(sub_images, key=lambda x: x.get_image_space().min_x)
        min_y_image = min(sub_images, key=lambda x: x.get_image_space().min_y)

        width_pixels = (
            max_x_image.get_image_space().max_x_pixels
            - min_x_image.get_image_space().min_x_pixels
        )
        height_pixels = (
            max_y_image.get_image_space().max_y_pixels
            - min_y_image.get_image_space().min_y_pixels
        )

        image = Image.new("RGBA", (width_pixels, height_pixels))

        for sub_image in sub_images:
            image.paste(
                sub_image.get_image(),
                (
                    abs(
                        min_x_image.get_image_space().min_x_pixels
                        - sub_image.get_image_space().min_x_pixels
                    ),
                    abs(
                        max_y_image.get_image_space().max_y_pixels
                        - sub_image.get_image_space().max_y_pixels
                    ),
                ),
                mask=sub_image.get_image().getchannel("A"),
            )

        return CompositePillowImage(sub_images, image)

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}({self.files})"

    def __len__(self) -> int:
        return len(self.files)
