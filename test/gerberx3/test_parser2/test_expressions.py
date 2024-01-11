"""tests based on Gerber expressions code samples."""

from __future__ import annotations

from test.gerberx3.test_parser2.common import make_parser2_test

test_sample = make_parser2_test(
    __file__,
    "test/assets/gerberx3/expressions",
    expression=True,
)
