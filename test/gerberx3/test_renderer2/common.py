"""Common elements of Rasterized2D tests."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from test.gerberx3.common import find_gerberx3_asset_files
from typing import TYPE_CHECKING, Callable

import pytest

from pygerber.gerberx3.parser2.parser2 import Parser2
from pygerber.gerberx3.renderer2.abstract import ImageRef
from pygerber.gerberx3.renderer2.raster import RasterRenderer2, RasterRenderer2Hooks
from pygerber.gerberx3.renderer2.svg import SvgRenderer2, SvgRenderer2Hooks
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def debug_dump_output_svg(out: ImageRef, dest_dir: Path) -> None:
    """Dump parser context to JSON file."""
    dest_dir.mkdir(exist_ok=True, parents=True)
    out.save_to(dest_dir / "dump.svg")


def render_svg(
    asset_loader: AssetLoader,
    src: str,
    dest: Path,
    *,
    expression: bool = False,
) -> None:
    """Tokenize gerber code and save debug output."""
    source = asset_loader.load_asset(src).decode("utf-8")
    if expression:
        stack = Tokenizer().tokenize_expressions(source)
    else:
        stack = Tokenizer().tokenize(source)

    parser = Parser2()
    cmd_buf = parser.parse(stack)
    ref = SvgRenderer2(SvgRenderer2Hooks(scale=Decimal("10"))).render(cmd_buf)

    debug_dump_output_svg(ref, dest)


def make_svg_renderer2_test(
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
    debug_output_directory = Path(test_file_path).parent / ".output" / "svg"

    @pytest.mark.parametrize(
        ("directory", "file_name"),
        sorted(find_gerberx3_asset_files(path_to_assets)),
    )
    def test_sample(
        asset_loader: AssetLoader,
        directory: str,
        file_name: str,
    ) -> None:
        dest = debug_output_directory / directory / Path(file_name).with_suffix("")
        dest.mkdir(mode=0o777, parents=True, exist_ok=True)
        render_svg(
            asset_loader,
            f"gerberx3/{directory}/{file_name}",
            dest,
            expression=expression,
        )

    return test_sample


def debug_dump_output_raster(out: ImageRef, dest_dir: Path) -> None:
    """Dump parser context to JSON file."""
    dest_dir.mkdir(exist_ok=True, parents=True)
    out.save_to(dest_dir / "dump.png")


def render_raster(
    asset_loader: AssetLoader,
    src: str,
    dest: Path,
    *,
    expression: bool = False,
) -> None:
    """Tokenize gerber code and save debug output."""

    config_overrides = asset_loader.load_asset_overrides(src)
    source = asset_loader.load_asset(src).decode("utf-8")
    if expression:
        stack = Tokenizer().tokenize_expressions(source)
    else:
        stack = Tokenizer().tokenize(source)

    parser = Parser2()
    cmd_buf = parser.parse(stack)
    ref = RasterRenderer2(
        RasterRenderer2Hooks(
            dpmm=int(config_overrides.get("raster", {}).get("dpmm", 40)),
        ),
    ).render(cmd_buf)

    debug_dump_output_raster(ref, dest)


def make_raster_renderer2_test(
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
    debug_output_directory = Path(test_file_path).parent / ".output" / "raster"

    @pytest.mark.parametrize(
        ("directory", "file_name"),
        sorted(find_gerberx3_asset_files(path_to_assets)),
    )
    def test_sample(
        asset_loader: AssetLoader,
        directory: str,
        file_name: str,
    ) -> None:
        dest = debug_output_directory / directory / Path(file_name).with_suffix("")
        dest.mkdir(mode=0o777, parents=True, exist_ok=True)
        src = f"gerberx3/{directory}/{file_name}"
        render_raster(
            asset_loader,
            src,
            dest,
            expression=expression,
        )

    return test_sample
