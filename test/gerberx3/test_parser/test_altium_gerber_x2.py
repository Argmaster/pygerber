"""tests based on AltiumGerberX2 board."""

from __future__ import annotations

from test.gerberx3.test_parser.common import make_parser_test

test_sample = make_parser_test(__file__, "test/assets/gerberx3/AltiumGerberX2")
