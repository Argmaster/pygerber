"""Utils for image operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PIL import Image


def replace_color(
    input_image: Image.Image,
    original: tuple[int, ...] | int,
    replacement: tuple[int, ...] | int,
    *,
    output_image_mode: str = "RGBA",
) -> Image.Image:
    """Replace `original` color from input image with `replacement` color."""
    if input_image.mode != output_image_mode:
        output_image = input_image.convert(output_image_mode)
    else:
        output_image = input_image.copy()

    for x in range(input_image.width):
        for y in range(input_image.height):
            if input_image.getpixel((x, y)) == original:
                output_image.putpixel((x, y), replacement)

    return output_image
