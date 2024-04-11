from __future__ import annotations

from pygerber.examples import ExamplesEnum, get_example_path
from pygerber.gerberx3.api.v2 import ColorScheme, GerberFile, PixelFormatEnum

GerberFile.from_file(
    get_example_path(ExamplesEnum.ShapeFlashes),
).parse().render_raster(
    "output.png",
    dpmm=100,
    color_scheme=ColorScheme.COPPER_ALPHA,
    pixel_format=PixelFormatEnum.RGBA,
)
