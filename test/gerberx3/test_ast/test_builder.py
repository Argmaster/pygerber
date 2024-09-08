from __future__ import annotations

from pygerber.gerberx3.ast.builder import GerberX3Builder


def test_circle_pad() -> None:
    builder = GerberX3Builder()

    d10 = builder.new_pad().circle(0.5)
    builder.add_pad(d10)

    builder.get_code()
