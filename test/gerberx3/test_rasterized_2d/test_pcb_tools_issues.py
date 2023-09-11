"""Rasterized2D tests based on KicadGerberX2 board."""

from __future__ import annotations

from test.gerberx3.test_rasterized_2d.common import make_rasterized_2d_test

test_sample = make_rasterized_2d_test(
    __file__,
    "test/assets/gerberx3/pcb_tools_issues",
    dpi=1000,
)
