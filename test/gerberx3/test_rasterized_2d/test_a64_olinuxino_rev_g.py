"""Tokenizer tests based on A64-OLinuXino-rev-G board."""

from __future__ import annotations

from test.gerberx3.test_rasterized_2d.common import make_rasterized_2d_test

test_sample = make_rasterized_2d_test(
    __file__,
    "test/assets/gerberx3/A64-OLinuXino-rev-G",
    dpi=500,
)
