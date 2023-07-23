"""Tokenizer tests based on A64-OLinuXino-rev-G board."""

from __future__ import annotations
from pathlib import Path

from typing import TYPE_CHECKING
from pygerber.backend.rasterized_2d.backend_cls import (
    Rasterized2DBackend,
    Rasterized2DBackendOptions,
)

from pygerber.gerberx3.parser.parser import Parser, ParserOptions
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from test.conftest import AssetLoader

IMAGE_DUMP = Path(__file__).parent / ".images" / "basic"
IMAGE_DUMP.mkdir(mode=0o777, parents=True, exist_ok=True)


def _draw_rasterized_2d(
    asset_loader: AssetLoader, src: str, dest: Path, dpi: int
) -> None:
    stack = Tokenizer().tokenize(
        asset_loader.load_asset(src).decode("utf-8"),
    )

    dest_apertures = dest / "apertures"
    dest_apertures.mkdir(mode=0o777, parents=True, exist_ok=True)

    parser_options = ParserOptions(
        backend=Rasterized2DBackend(
            options=Rasterized2DBackendOptions(
                dpi=dpi,
                dump_apertures=dest_apertures,
            )
        )
    )

    parser = Parser(stack, options=parser_options)
    draws = parser.parse()

    result = draws.draw()
    result.save(dest / "output.png")


def test_rasterized_2d_source_0(asset_loader: AssetLoader, tmp_path: Path) -> None:
    """Rasterized2D rendering test based on sample-0/source.grb file."""
    _draw_rasterized_2d(
        asset_loader,
        "gerberx3/basic/sample-0/source.grb",
        IMAGE_DUMP / "source_0",
        dpi=1000,
    )


def test_rasterized_2d_source_0_b(asset_loader: AssetLoader, tmp_path: Path) -> None:
    """Rasterized2D rendering test based on sample-0/source_b.grb file."""
    _draw_rasterized_2d(
        asset_loader,
        "gerberx3/basic/sample-0/source_b.grb",
        IMAGE_DUMP / "source_0_b",
        dpi=1000,
    )


def test_rasterized_2d_source_0_c(asset_loader: AssetLoader, tmp_path: Path) -> None:
    """Rasterized2D rendering test based on sample-0/source_c.grb file."""
    _draw_rasterized_2d(
        asset_loader,
        "gerberx3/basic/sample-0/source_c.grb",
        IMAGE_DUMP / "source_0_c",
        dpi=1000,
    )


def test_rasterized_2d_source_0_d(asset_loader: AssetLoader, tmp_path: Path) -> None:
    """Rasterized2D rendering test based on sample-0/source_d.grb file."""
    _draw_rasterized_2d(
        asset_loader,
        "gerberx3/basic/sample-0/source_d.grb",
        IMAGE_DUMP / "source_0_d",
        dpi=1000,
    )


def test_rasterized_2d_source_0_e(asset_loader: AssetLoader, tmp_path: Path) -> None:
    """Rasterized2D rendering test based on sample-0/source_e.grb file."""
    _draw_rasterized_2d(
        asset_loader,
        "gerberx3/basic/sample-0/source_e.grb",
        IMAGE_DUMP / "source_0_e",
        dpi=1000,
    )


def test_rasterized_2d_source_0_f(asset_loader: AssetLoader, tmp_path: Path) -> None:
    """Rasterized2D rendering test based on sample-0/source_f.grb file."""
    _draw_rasterized_2d(
        asset_loader,
        "gerberx3/basic/sample-0/source_f.grb",
        IMAGE_DUMP / "source_0_f",
        dpi=1000,
    )


def test_rasterized_2d_source_0_g(asset_loader: AssetLoader, tmp_path: Path) -> None:
    """Rasterized2D rendering test based on sample-0/source_g.grb file."""
    _draw_rasterized_2d(
        asset_loader,
        "gerberx3/basic/sample-0/source_g.grb",
        IMAGE_DUMP / "source_0_g",
        dpi=1000,
    )


def test_rasterized_2d_source_1(asset_loader: AssetLoader, tmp_path: Path) -> None:
    """Rasterized2D rendering test based on sample-1/source.grb file."""
    _draw_rasterized_2d(
        asset_loader,
        "gerberx3/basic/sample-1/source.grb",
        IMAGE_DUMP / "source_1",
        dpi=20000,
    )


def test_rasterized_2d_source_2(asset_loader: AssetLoader, tmp_path: Path) -> None:
    """Rasterized2D rendering test based on sample-2/source.grb file."""
    _draw_rasterized_2d(
        asset_loader,
        "gerberx3/basic/sample-2/source.grb",
        IMAGE_DUMP / "source_2",
        dpi=1000,
    )


def test_rasterized_2d_source_2_b(asset_loader: AssetLoader, tmp_path: Path) -> None:
    """Rasterized2D rendering test based on sample-2/source_b.grb file."""
    _draw_rasterized_2d(
        asset_loader,
        "gerberx3/basic/sample-2/source_b.grb",
        IMAGE_DUMP / "source_2_b",
        dpi=1000,
    )
