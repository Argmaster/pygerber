from __future__ import annotations

from pygerber.examples import ExamplesEnum, load_example
from pygerber.gerberx3.api.v2 import GerberFile

source_code = load_example(ExamplesEnum.UCAMCO_ex_2_Shapes)
GerberFile.from_str(source_code).parse().render_svg("output.svg")
