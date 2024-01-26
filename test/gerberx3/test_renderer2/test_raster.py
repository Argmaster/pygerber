"""Renderer tests based on auto loaded tests asserts.."""

from __future__ import annotations

from test.gerberx3.test_renderer2.common import make_raster_renderer2_test

test_a64_o_linu_xino_rev_g = make_raster_renderer2_test(
    __file__,
    "test/assets/gerberx3/A64-OLinuXino-rev-G",
)
test_altium_gerber_x2 = make_raster_renderer2_test(
    __file__,
    "test/assets/gerberx3/AltiumGerberX2",
)

test_atmega328_motor_board = make_raster_renderer2_test(
    __file__,
    "test/assets/gerberx3/ATMEGA328-Motor-Board",
)
test_basic = make_raster_renderer2_test(
    __file__,
    "test/assets/gerberx3/basic",
)
test_expressions = make_raster_renderer2_test(
    __file__,
    "test/assets/gerberx3/expressions",
    expression=True,
)
test_kicad_arduino = make_raster_renderer2_test(
    __file__,
    "test/assets/gerberx3/kicad/arduino",
)
test_kicad_gerber_x2 = make_raster_renderer2_test(
    __file__,
    "test/assets/gerberx3/KicadGerberX2",
)
test_kicad_hello = make_raster_renderer2_test(
    __file__,
    "test/assets/gerberx3/kicad/hello",
)
test_pcb_tools_issues = make_raster_renderer2_test(
    __file__,
    "test/assets/gerberx3/pcb_tools_issues",
)
