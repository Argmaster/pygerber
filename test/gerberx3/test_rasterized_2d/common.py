"""Common elements of Rasterized2D tests."""

from __future__ import annotations

from pathlib import Path
from test.gerberx3.common import find_gerberx3_asset_files
from typing import TYPE_CHECKING, Callable

import pytest

from pygerber.backend.rasterized_2d.backend_cls import (
    Rasterized2DBackend,
    Rasterized2DBackendOptions,
)
from pygerber.gerberx3.parser.parser import Parser, ParserOptions
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def draw_rasterized_2d(
    asset_loader: AssetLoader,
    src: str,
    dest: Path,
    dpi: int,
) -> None:
    """Draw 2D rasterized image and save it."""
    stack = Tokenizer().tokenize_expressions(
        asset_loader.load_asset(src).decode("utf-8"),
    )

    dest_apertures = dest / "apertures"
    dest_apertures.mkdir(mode=0o777, parents=True, exist_ok=True)

    parser_options = ParserOptions(
        backend=Rasterized2DBackend(
            options=Rasterized2DBackendOptions(
                dpi=dpi,
                dump_apertures=dest_apertures,
                include_debug_padding=True,
                include_bounding_boxes=True,
            ),
        ),
    )

    parser = Parser(options=parser_options)
    draws = parser.parse(stack)

    result = draws.draw()
    result.save(dest / "output.png")


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
