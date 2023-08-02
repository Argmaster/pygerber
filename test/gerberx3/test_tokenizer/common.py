"""Common elements of Rasterized2D tests."""

from __future__ import annotations
from pathlib import Path

from typing import TYPE_CHECKING, Callable

import pytest


from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer
from test.gerberx3.common import find_gerberx3_asset_files

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def tokenize(
    asset_loader: AssetLoader,
    src: str,
    dest: Path,
    *,
    expression: bool = False,
) -> None:
    """Tokenize gerber code and save debug output"""
    source = asset_loader.load_asset(src).decode("utf-8")
    if expression:
        stack = Tokenizer().tokenize_expressions(source)
    else:
        stack = Tokenizer().tokenize(source)

    with (dest / "output.grb").open("wt") as file:
        for token in stack:
            file.write(f"{token}\n")

    with (dest / "output.repr.txt").open("wt") as file:
        for token in stack:
            file.write(f"{token.get_debug_format()}\n")


def make_tokenizer_test(
    test_file_path: str,
    path_to_assets: str,
    *,
    expression: bool = False,
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
    def test_sample(
        asset_loader: AssetLoader,
        directory: str,
        file_name: str,
    ) -> None:
        """Rasterized2D rendering test based on sample files."""
        dest = image_dump / directory / Path(file_name).with_suffix("")
        dest.mkdir(mode=0o777, parents=True, exist_ok=True)
        tokenize(
            asset_loader,
            f"gerberx3/{directory}/{file_name}",
            dest,
            expression=expression,
        )

    return test_sample
