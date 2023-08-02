"""Tokenizer tests based on Gerber expressions code samples."""

from __future__ import annotations


from test.gerberx3.test_rasterized_2d.common import make_rasterized_2d_test


test_sample = make_rasterized_2d_test(
    __file__, "test/assets/gerberx3/expressions", dpi=500
)
