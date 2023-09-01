"""Tokenizer tests based on Gerber basic code samples."""

from __future__ import annotations

from test.gerberx3.test_rasterized_2d.common import (
    make_rasterized_2d_test_with_reference,
)

test_sample = make_rasterized_2d_test_with_reference(
    __file__,
    "test/assets/gerberx3/basic",
    dpi=2000,
)
