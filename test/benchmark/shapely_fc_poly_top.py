from __future__ import annotations

import cProfile
from pathlib import Path
from typing import cast

from pygerber.gerber.compiler import compile
from pygerber.gerber.parser import parse
from pygerber.vm import render
from pygerber.vm.shapely import ShapelyResult
from test.assets.gerberx3.FcPoly_Test import FcPoly_Test

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


def benchmark() -> None:
    ast = parse(FcPoly_Test.top.load())
    rvmc = compile(ast)
    result = cast("ShapelyResult", render(rvmc, backend="shapely"))
    result.save_svg(THIS_DIRECTORY / "#FcPoly_bottom.svg")


if __name__ == "__main__":
    cProfile.run("benchmark()", THIS_FILE.with_suffix(".prof").as_posix())
