"""Tokenizer tests based on AltiumGerberX2 board."""

from __future__ import annotations

from typing import TYPE_CHECKING


from test.gerberx3.test_rasterized_2d.common import make_rasterized_2d_test

if TYPE_CHECKING:
    pass


test_sample = make_rasterized_2d_test(
    __file__, "test/assets/gerberx3/AltiumGerberX2", dpi=500
)
