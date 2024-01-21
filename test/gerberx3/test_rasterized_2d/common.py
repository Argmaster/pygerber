"""Common elements of Rasterized2D tests."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from test.gerberx3.common import find_gerberx3_asset_files
from typing import TYPE_CHECKING, Callable

import pytest
from PIL import Image, ImageDraw

from pygerber.backend.rasterized_2d.backend_cls import (
    Rasterized2DBackend,
    Rasterized2DBackendOptions,
)
from pygerber.gerberx3.api import ColorScheme
from pygerber.gerberx3.parser.parser import Parser, ParserOptions
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def draw_rasterized_2d(
    asset_loader: AssetLoader,
    src: str,
    dest: Path,
    dpi: int,
    *,
    is_debug_enabled: bool = True,
) -> BytesIO:
    """Draw 2D rasterized image and save it."""
    stack = Tokenizer().tokenize_expressions(
        asset_loader.load_asset(src).decode("utf-8"),
    )

    dest_apertures = dest / "apertures"
    dest_apertures.mkdir(mode=0o777, parents=True, exist_ok=True)

    config_overrides = asset_loader.load_asset_overrides(src)
    dpi = config_overrides.get("dpi", dpi)

    parser_options = ParserOptions(
        backend=Rasterized2DBackend(
            options=Rasterized2DBackendOptions(
                dpi=dpi,
                color_scheme=ColorScheme.DEBUG_1,
                dump_apertures=dest_apertures if is_debug_enabled else None,
                include_debug_padding=is_debug_enabled,
                include_bounding_boxes=is_debug_enabled,
            ),
        ),
    )

    parser = Parser(options=parser_options)
    draws = parser.parse(stack)

    result = draws.draw()
    output_buffer = BytesIO()
    result.save(output_buffer, format="png")

    output_buffer.seek(0)
    output_image_bytes = output_buffer.read()

    file_path = dest / "output.png"
    file_path.write_bytes(output_image_bytes)

    output_buffer.seek(0)
    return output_buffer


def make_rasterized_2d_test(
    test_file_path: str,
    path_to_assets: str,
    dpi: int = 2000,
) -> Callable[..., None]:
    """Create parametrized test case for all files from path_to_assets.

    All Gerber files from `path_to_assets` will be included as separate test cases
    thanks to use of `@pytest.mark.parametrize`.

    Parameters
    ----------
    test_file_path : str
        Path to test file, simply use `__file__` variable from module global scope.
    path_to_assets : str
        Path to assets directory, originating from the root of repository, eg.
        `test/assets/gerberx3/basic`.

    Returns
    -------
    Callable[..., None]
        Test callable. Must be assigned to variable with name starting with `test_`.
    """
    image_dump = Path(test_file_path).parent / ".output"

    @pytest.mark.parametrize(
        ("directory", "file_name"),
        sorted(find_gerberx3_asset_files(path_to_assets)),
    )
    def test_sample(asset_loader: AssetLoader, directory: str, file_name: str) -> None:
        """Rasterized2D rendering test based on sample files."""
        dest = image_dump / directory / Path(file_name).with_suffix("")
        dest.mkdir(mode=0o777, parents=True, exist_ok=True)
        draw_rasterized_2d(
            asset_loader,
            f"gerberx3/{directory}/{file_name}",
            dest,
            dpi=dpi,
        )

    return test_sample


def make_rasterized_2d_test_with_reference(
    test_file_path: str,
    path_to_assets: str,
    dpi: int = 2000,
) -> Callable[..., None]:
    """Create parametrized test case for all files from path_to_assets.

    All Gerber files from `path_to_assets` will be included as separate test cases
    thanks to use of `@pytest.mark.parametrize`.

    Parameters
    ----------
    test_file_path : str
        Path to test file, simply use `__file__` variable from module global scope.
    path_to_assets : str
        Path to assets directory, originating from the root of repository, eg.
        `test/assets/gerberx3/basic`.

    Returns
    -------
    Callable[..., None]
        Test callable. Must be assigned to variable with name starting with `test_`.
    """
    image_dump = Path(test_file_path).parent / ".output_reference"
    image_diff_dir = Path(test_file_path).parent / ".diff"
    image_reference = Path(test_file_path).parent / "reference"

    @pytest.mark.parametrize(
        ("directory", "file_name"),
        sorted(find_gerberx3_asset_files(path_to_assets)),
    )
    def test_sample(asset_loader: AssetLoader, directory: str, file_name: str) -> None:
        """Rasterized2D rendering test based on sample files."""
        image_dump_dest = image_dump / directory / Path(file_name).with_suffix("")
        image_dump_dest.mkdir(mode=0o777, parents=True, exist_ok=True)

        rendered_image_buffer = draw_rasterized_2d(
            asset_loader,
            f"gerberx3/{directory}/{file_name}",
            image_dump_dest,
            dpi=dpi,
            is_debug_enabled=False,
        )
        rendered_image = Image.open(rendered_image_buffer).convert("RGBA")

        reference_image = _get_reference_image(directory, file_name, rendered_image)

        if reference_image != rendered_image:
            diff_image_dest = (
                image_diff_dir / directory / Path(file_name).with_suffix("")
            )
            diff_image_dest.mkdir(mode=0o777, parents=True, exist_ok=True)
            diff_image = highlight_differences(rendered_image, reference_image)

            diff_image.save(diff_image_dest / "diff.png")

            msg = "Image mismatch."
            raise ValueError(msg)

    def _get_reference_image(
        directory: str,
        file_name: str,
        alt_image: Image.Image,
    ) -> Image.Image:
        image_reference_dest = (
            image_reference / directory / Path(file_name).with_suffix("")
        )
        image_reference_dest.mkdir(mode=0o777, parents=True, exist_ok=True)
        reference_image_path = image_reference_dest / "image.png"

        if not reference_image_path.exists():
            alt_image.save(reference_image_path)

        return Image.open(reference_image_path).convert(
            "RGBA",
        )

    return test_sample


def pad_and_center(
    img: Image.Image,
    target_width: int,
    target_height: int,
    fill_color: tuple[int, ...] | int,
) -> Image.Image:
    """
    Pad and center the image to the target dimensions.
    """
    result = Image.new("RGBA", (target_width, target_height), fill_color)
    left = (target_width - img.width) // 2
    top = (target_height - img.height) // 2
    result.paste(img, (left, top))
    return result


def highlight_differences(first: Image.Image, second: Image.Image) -> Image.Image:
    """
    Highlight the differences between two images.
    """
    max_width = max(first.width, second.width)
    max_height = max(first.height, second.height)

    # Pad and center images
    img1_centered = pad_and_center(first, max_width, max_height, (0, 0, 0, 0))
    img2_centered = pad_and_center(second, max_width, max_height, (0, 0, 0, 0))

    diff_img = Image.new("RGBA", (max_width, max_height))

    draw = ImageDraw.Draw(diff_img)
    for x in range(max_width):
        for y in range(max_height):
            r1, g1, b1, a1 = img1_centered.getpixel((x, y))
            r2, g2, b2, a2 = img2_centered.getpixel((x, y))
            draw.point(
                (x, y),
                fill=(
                    abs(r1 - r2),
                    abs(g1 - g2),
                    abs(b1 - b2),
                    255 - abs(a1 - a2),
                ),
            )

    return diff_img
