from __future__ import annotations

import pytest

from pygerber.gerber.ast.builder import GerberX3Builder


@pytest.fixture
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


class TestCustomPads:
    def test_circle_0_0(self, builder: GerberX3Builder, default_header: str) -> None:
        d10 = builder.new_pad().custom().add_circle(1, (0, 0)).create()
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%AMM0*
1,1.0,1.0,0.0,0.0,0.0*%
%ADD10M0*%
D10*
X0Y0D03*
M02*
"""
        )

    def test_add_circle_5_5(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        d10 = builder.new_pad().custom().add_circle(1, (5, 5), rotation=60).create()
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%AMM0*
1,1.0,1.0,5.0,5.0,60.0*%
%ADD10M0*%
D10*
X0Y0D03*
M02*
"""
        )

    def test_cut_circle_5_5(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        d10 = builder.new_pad().custom().cut_circle(1, (5, 5), rotation=60).create()
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%AMM0*
1,0.0,1.0,5.0,5.0,60.0*%
%ADD10M0*%
D10*
X0Y0D03*
M02*
"""
        )

    def test_add_vector_line_0_0_1_1(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        d10 = (
            builder.new_pad()
            .custom()
            .add_vector_line(1, (0, 0), (1, 1), rotation=30)
            .create()
        )
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%AMM0*
20,1.0,1.0,0.0,0.0,1.0,1.0,30.0*%
%ADD10M0*%
D10*
X0Y0D03*
M02*
"""
        )

    def test_cut_vector_line_0_0_1_1(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        d10 = (
            builder.new_pad()
            .custom()
            .cut_vector_line(1, (0, 0), (1, 1), rotation=30)
            .create()
        )
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%AMM0*
20,0.0,1.0,0.0,0.0,1.0,1.0,30.0*%
%ADD10M0*%
D10*
X0Y0D03*
M02*
"""
        )

    def test_add_center_line_1_2_0_0(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        d10 = builder.new_pad().custom().add_center_line(1, 2, (0, 0), 30).create()
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%AMM0*
21,1.0,1.0,2.0,0.0,0.0,30.0*%
%ADD10M0*%
D10*
X0Y0D03*
M02*
"""
        )

    def test_cut_center_line_1_2_0_0(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        d10 = builder.new_pad().custom().cut_center_line(1, 2, (0, 0), 30).create()
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%AMM0*
21,0.0,1.0,2.0,0.0,0.0,30.0*%
%ADD10M0*%
D10*
X0Y0D03*
M02*
"""
        )

    def test_add_outline_4p(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        d10 = (
            builder.new_pad()
            .custom()
            .add_outline([(0, 0), (1, 0), (1, 1), (0, 1)], rotation=30)
            .create()
        )
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%AMM0*
4,1.0,4.0,0.0,1.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0,1.0,30.0*%
%ADD10M0*%
D10*
X0Y0D03*
M02*
"""
        )

    def test_cut_outline_4p(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        d10 = (
            builder.new_pad()
            .custom()
            .cut_outline([(0, 0), (1, 0), (1, 1), (0, 1)], rotation=30)
            .create()
        )
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%AMM0*
4,0.0,4.0,0.0,1.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0,1.0,30.0*%
%ADD10M0*%
D10*
X0Y0D03*
M02*
"""
        )

    def test_add_polygon_6p(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        d10 = (
            builder.new_pad()
            .custom()
            .add_polygon(6, (0, 0), outer_diameter=1.0, rotation=30)
            .create()
        )
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%AMM0*
5,1.0,6.0,0.0,0.0,1.0,30.0*%
%ADD10M0*%
D10*
X0Y0D03*
M02*
"""
        )

    def test_cut_polygon_6p(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        d10 = (
            builder.new_pad()
            .custom()
            .cut_polygon(6, (0, 0), outer_diameter=1.0, rotation=30)
            .create()
        )
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%AMM0*
5,0.0,6.0,0.0,0.0,1.0,30.0*%
%ADD10M0*%
D10*
X0Y0D03*
M02*
"""
        )

    def test_one_complicated(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        d10 = (
            builder.new_pad()
            .custom()
            .add_circle(1, (0, 0))
            .add_circle(1, (1, 1))
            .add_vector_line(1, (0, 0), (1, 1), rotation=30)
            .add_center_line(1, 2, (0, 0), 30)
            .add_outline([(0, 0), (1, 0), (1, 1), (0, 1)], rotation=30)
            .add_polygon(6, (0, 0), outer_diameter=1.0, rotation=30)
            .create()
        )
        builder.add_pad(d10, (0, 0))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%AMM0*
1,1.0,1.0,0.0,0.0,0.0*
1,1.0,1.0,1.0,1.0,0.0*
20,1.0,1.0,0.0,0.0,1.0,1.0,30.0*
21,1.0,1.0,2.0,0.0,0.0,30.0*
4,1.0,4.0,0.0,1.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0,1.0,30.0*
5,1.0,6.0,0.0,0.0,1.0,30.0*%
%ADD10M0*%
D10*
X0Y0D03*
M02*
"""
        )

    def test_two_complicated(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        d10 = (
            builder.new_pad()
            .custom()
            .add_circle(1, (0, 0))
            .add_circle(1, (1, 1))
            .create()
        )
        builder.add_pad(d10, (0, 0))
        d11 = (
            builder.new_pad()
            .custom()
            .add_vector_line(1, (0, 0), (1, 1), rotation=30)
            .add_center_line(1, 2, (0, 0), 30)
            .add_outline([(0, 0), (1, 0), (1, 1), (0, 1)], rotation=30)
            .add_polygon(6, (0, 0), outer_diameter=1.0, rotation=30)
            .create()
        )
        builder.add_pad(d11, (3, 3))

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%AMM0*
1,1.0,1.0,0.0,0.0,0.0*
1,1.0,1.0,1.0,1.0,0.0*%
%AMM1*
20,1.0,1.0,0.0,0.0,1.0,1.0,30.0*
21,1.0,1.0,2.0,0.0,0.0,30.0*
4,1.0,4.0,0.0,1.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0,1.0,30.0*
5,1.0,6.0,0.0,0.0,1.0,30.0*%
%ADD10M0*%
%ADD11M1*%
D10*
X0Y0D03*
D11*
X3000000Y3000000D03*
M02*
"""
        )


class TestTraces:
    def test_one_trace(self, builder: GerberX3Builder, default_header: str) -> None:
        builder.add_trace(0.1, (0, 0), (1, 1))
        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.1*%
D10*
X1000000Y1000000D01*
M02*
"""
        )

    def test_two_traces_same_width(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        builder.add_trace(0.1, (0, 0), (1, 1))
        builder.add_trace(0.1, (1, 1), (1, 2))
        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.1*%
D10*
X1000000Y1000000D01*
X1000000Y2000000D01*
M02*
"""
        )

    def test_two_traces_different_width(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        builder.add_trace(0.1, (0, 0), (1, 1))
        builder.add_trace(0.2, (1, 1), (1, 2))
        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.1*%
%ADD11C,0.2*%
D10*
X1000000Y1000000D01*
D11*
X1000000Y2000000D01*
M02*
"""
        )

    def test_three_traces(self, builder: GerberX3Builder, default_header: str) -> None:
        builder.add_trace(0.1, (0, 0), (1, 1))
        builder.add_trace(0.2, (1, 1), (1, 2))
        builder.add_trace(0.1, (1, 2), (2, 1))
        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.1*%
%ADD11C,0.2*%
D10*
X1000000Y1000000D01*
D11*
X1000000Y2000000D01*
D10*
X2000000Y1000000D01*
M02*
"""
        )

    def test_two_traces_discontinued(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        builder.add_trace(0.1, (0, 0), (1, 1))
        builder.add_trace(0.1, (2, 2), (3, 3))
        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,0.1*%
D10*
X1000000Y1000000D01*
X2000000Y2000000D02*
X3000000Y3000000D01*
M02*
"""
        )

    def test_trace_connect_two_pads(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        pad = builder.new_pad().circle(1.0)

        pad0 = builder.add_pad(pad, (0, 0))
        pad1 = builder.add_pad(pad, (2, 2))

        builder.add_trace(0.1, pad0, pad1)

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,1.0*%
%ADD11C,0.1*%
D10*
X0Y0D03*
X2000000Y2000000D03*
D11*
X0Y0D02*
X2000000Y2000000D01*
M02*
"""
        )

    def test_two_trace_connect_two_pads(
        self, builder: GerberX3Builder, default_header: str
    ) -> None:
        pad = builder.new_pad().circle(1.0)

        pad0 = builder.add_pad(pad, (0, 0))
        pad1 = builder.add_pad(pad, (2, 2))

        trace0 = builder.add_trace(0.1, pad0, (1, 1))
        builder.add_trace(0.1, trace0, pad1)

        assert (
            builder.get_code().dumps()
            == f"""{default_header}
%ADD10C,1.0*%
%ADD11C,0.1*%
D10*
X0Y0D03*
X2000000Y2000000D03*
D11*
X0Y0D02*
X1000000Y1000000D01*
X2000000Y2000000D01*
M02*
"""
        )
