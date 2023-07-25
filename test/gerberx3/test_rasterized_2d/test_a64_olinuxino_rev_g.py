"""Tokenizer tests based on A64-OLinuXino-rev-G board."""

from __future__ import annotations
from pathlib import Path

from typing import TYPE_CHECKING

import pytest
from test.gerberx3.common import find_gerberx3_asset_files

from test.gerberx3.test_rasterized_2d.common import draw_rasterized_2d

if TYPE_CHECKING:
    from test.conftest import AssetLoader

IMAGE_DUMP = Path(__file__).parent / ".output"
IMAGE_DUMP.mkdir(mode=0o777, parents=True, exist_ok=True)


@pytest.mark.parametrize(
    ["directory", "file_name"],
    sorted(find_gerberx3_asset_files("test/assets/gerberx3/A64-OLinuXino-rev-G")),
)
def test_sample(asset_loader: AssetLoader, directory: str, file_name: str) -> None:
    """Rasterized2D rendering test based on sample files."""
    draw_rasterized_2d(
        asset_loader,
        f"gerberx3/{directory}/{file_name}",
        IMAGE_DUMP / directory / file_name[:-4],
        dpi=1000,
    )
