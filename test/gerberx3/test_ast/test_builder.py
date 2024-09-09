from __future__ import annotations

import pytest

from pygerber.gerberx3.ast.builder import GerberX3Builder


@pytest.fixture()
def builder() -> GerberX3Builder:
    return GerberX3Builder()


@pytest.fixture(scope="session")
def default_header() -> str:
    return "%FSLAX46Y46*%\n%MOMM*%"


class TestCirclePad:
    def test_one_dark(self, builder: GerberX3Builder, default_header: str) -> None:
        d10 = builder.new_pad().circle(0.5)
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.5*%
D10*
X0Y0D03*
M02*
"""
        )

    def test_two_same_dark(self, builder: GerberX3Builder, default_header: str) -> None:
        d10 = builder.new_pad().circle(0.5)
        builder.add_pad(d10, (0, 0))
        builder.add_pad(d10, (0, 2.0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.5*%
D10*
X0Y0D03*
X0Y2000000D03*
M02*
"""
        )

    def test_two_different_dark(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        d10 = builder.new_pad().circle(0.5)
        d11 = builder.new_pad().circle(0.4)
        builder.add_pad(d10, (0, 0))
        builder.add_pad(d11, (0, 2.0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.5*%
%ADD11C,0.4*%
D10*
X0Y0D03*
D11*
X0Y2000000D03*
M02*
"""
        )

    def test_one_clear(self, builder: GerberX3Builder, default_header: str) -> None:
        d10 = builder.new_pad().circle(0.5)
        builder.add_cutout_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.5*%
D10*
%LPC*%
X0Y0D03*
M02*
"""
        )

    def test_two_same_dark_clear(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        d10 = builder.new_pad().circle(0.5)
        builder.add_pad(d10, (0, 0))
        builder.add_cutout_pad(d10, (0, 2.0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.5*%
D10*
X0Y0D03*
%LPC*%
X0Y2000000D03*
M02*
"""
        )


def test_rectangle_pad(builder: GerberX3Builder, default_header: str) -> None:
    d10 = builder.new_pad().rectangle(0.4, 0.7)
    builder.add_pad(d10, (0, 0))

    assert (
        builder.get_code().dumps()
        == f"""{default_header}
%ADD10R,0.4X0.7*%
D10*
X0Y0D03*
M02*
"""
    )


def test_rounded_rectangle_pad(builder: GerberX3Builder, default_header: str) -> None:
    d10 = builder.new_pad().rounded_rectangle(0.4, 0.7)
    builder.add_pad(d10, (0, 0))

    assert (
        builder.get_code().dumps()
        == f"""{default_header}
%ADD10O,0.4X0.7*%
D10*
X0Y0D03*
M02*
"""
    )


def test_regular_polygon_pad(builder: GerberX3Builder, default_header: str) -> None:
    builder = GerberX3Builder()

    d10 = builder.new_pad().regular_polygon(0.5, 6, 0)
    builder.add_pad(d10, (0, 0))

    assert (
        builder.get_code().dumps()
        == f"""{default_header}
%ADD10P,0.5X6X0.0*%
D10*
X0Y0D03*
M02*
"""
    )


class TestChangeTransform:
    def test_rotation(self, builder: GerberX3Builder, default_header: str) -> None:
        d10 = builder.new_pad().circle(0.5)
        builder.add_pad(d10, (0, 0))
        builder.add_pad(d10, (0, 2.0), rotation=90)
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.5*%
D10*
X0Y0D03*
%LR90.0*%
X0Y2000000D03*
%LR0.0*%
X0Y0D03*
M02*
"""
        )

    def test_mirror_x(self, builder: GerberX3Builder, default_header: str) -> None:
        d10 = builder.new_pad().circle(0.5)
        builder.add_pad(d10, (0, 0))
        builder.add_pad(d10, (0, 2.0), mirror_x=True)
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.5*%
D10*
X0Y0D03*
%LMX*%
X0Y2000000D03*
%LMN*%
X0Y0D03*
M02*
"""
        )

    def test_mirror_y(self, builder: GerberX3Builder, default_header: str) -> None:
        d10 = builder.new_pad().circle(0.5)
        builder.add_pad(d10, (0, 0))
        builder.add_pad(d10, (0, 2.0), mirror_y=True)
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.5*%
D10*
X0Y0D03*
%LMY*%
X0Y2000000D03*
%LMN*%
X0Y0D03*
M02*
"""
        )

    def test_mirror_xy(self, builder: GerberX3Builder, default_header: str) -> None:
        d10 = builder.new_pad().circle(0.5)
        builder.add_pad(d10, (0, 0))
        builder.add_pad(d10, (0, 2.0), mirror_x=True, mirror_y=True)
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.5*%
D10*
X0Y0D03*
%LMXY*%
X0Y2000000D03*
%LMN*%
X0Y0D03*
M02*
"""
        )

    def test_mirror_switch(self, builder: GerberX3Builder, default_header: str) -> None:
        d10 = builder.new_pad().circle(0.5)
        builder.add_pad(d10, (0, 0))
        builder.add_pad(d10, (0, 0), mirror_x=True)
        builder.add_pad(d10, (0, 0), mirror_x=True)
        builder.add_pad(d10, (0, 0), mirror_y=True)
        builder.add_pad(d10, (0, 2.0), mirror_x=True, mirror_y=True)
        builder.add_pad(d10, (0, 0), mirror_y=True)
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.5*%
D10*
X0Y0D03*
%LMX*%
X0Y0D03*
X0Y0D03*
%LMY*%
X0Y0D03*
%LMXY*%
X0Y2000000D03*
%LMY*%
X0Y0D03*
%LMN*%
X0Y0D03*
M02*
"""
        )

    def test_scale(self, builder: GerberX3Builder, default_header: str) -> None:
        d10 = builder.new_pad().circle(0.5)
        builder.add_pad(d10, (0, 0))
        builder.add_pad(d10, (0, 2.0), scale=2.0)
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.5*%
D10*
X0Y0D03*
%LS2.0*%
X0Y2000000D03*
%LS1.0*%
X0Y0D03*
M02*
"""
        )
