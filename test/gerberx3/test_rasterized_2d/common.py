"""Common elements of Rasterized2D tests."""

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


def draw_rasterized_2d(
    asset_loader: AssetLoader, src: str, dest: Path, dpi: int
) -> None:
    """Draw 2D rasterized image and save it."""
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
                include_debug_padding=True,
                include_bounding_boxes=True,
            )
        )
    )

    parser = Parser(stack, options=parser_options)
    draws = parser.parse()

    result = draws.draw()
    result.save(dest / "output.png")
