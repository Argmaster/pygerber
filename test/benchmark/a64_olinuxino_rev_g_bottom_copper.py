from __future__ import annotations

import cProfile
from pathlib import Path
from typing import cast

import test.assets.gerberx3.A64_OLinuXino_rev_G as A64_OlinuXino_Rev_G
from pygerber.gerber.compiler import compile
from pygerber.gerber.parser import parse
from pygerber.vm import render
from pygerber.vm.pillow.vm import PillowResult

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


def benchmark() -> None:
    ast = parse(A64_OlinuXino_Rev_G.A64_OlinuXino_Rev_G_B_Cu.load())
    rvmc = compile(ast)
    result = cast("PillowResult", render(rvmc, dpmm=100))
    result.get_image().save(THIS_DIRECTORY / "#A64_OLinuXino_rev_G_bottom_copper.png")


if __name__ == "__main__":
    cProfile.run("benchmark()", THIS_FILE.with_suffix(".prof").as_posix())
