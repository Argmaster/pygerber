from __future__ import annotations

from pathlib import Path

from pygerber.gerberx3.api import (
    ColorScheme,
    Rasterized2DLayer,
    Rasterized2DLayerParams,
)


def render() -> None:
    source_path = (
        Path.cwd()
        / "test/assets/gerberx3/A64-OLinuXino-rev-G/A64-OlinuXino_Rev_G-B_Cu.gbr"
    )

    Rasterized2DLayer(
        options=Rasterized2DLayerParams(
            source_path=source_path,
            colors=ColorScheme.COPPER_ALPHA,
        ),
    ).render().save("output.png")


if __name__ == "__main__":
    render()
