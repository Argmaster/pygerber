from __future__ import annotations

from pygerber.examples import ExamplesEnum, get_example_path
from pygerber.gerberx3.api.v2 import GerberFile

GerberFile.from_file(
    get_example_path(ExamplesEnum.UCAMCO_ex_2_Shapes),
).parse().render_raster("output.jpg")
