"""Tokenizer tests based on KicadGerberX2 board."""

from __future__ import annotations

from test.gerberx3.test_tokenizer.common import make_tokenizer_test


test_sample = make_tokenizer_test(__file__, "test/assets/gerberx3/KicadGerberX2")
