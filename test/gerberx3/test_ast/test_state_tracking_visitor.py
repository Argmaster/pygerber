from __future__ import annotations

from inspect import isclass
from typing import TYPE_CHECKING, ClassVar, List

import pytest

from pygerber.gerberx3.ast.errors import (
    ApertureNotSelectedError,
    PackedCoordinateTooLongError,
    PackedCoordinateTooShortError,
)
from pygerber.gerberx3.ast.nodes import (
    AB,
    ADC,
    ADO,
    ADP,
    ADR,
    AM,
    D01,
    D03,
    FS,
    G01,
    G02,
    G03,
    G36,
    G37,
    G74,
    G75,
    ABclose,
    ABopen,
    ADmacro,
    AMclose,
    AMopen,
    CoordinateI,
    CoordinateJ,
    CoordinateX,
    CoordinateY,
    Dnn,
    Node,
    PackedCoordinateStr,
    TA_AperFunction,
    TA_DrillTolerance,
    TF_FileFunction,
)
from pygerber.gerberx3.ast.nodes.enums import (
    AperFunction,
    CoordinateNotation,
    FileFunction,
    Zeros,
)
from pygerber.gerberx3.ast.nodes.types import ApertureIdStr
from pygerber.gerberx3.ast.state_tracking_visitor import (
    CoordinateFormat,
    StateTrackingVisitor,
)

if TYPE_CHECKING:
    from pytest_mock import MockerFixture
    from typing_extensions import TypeAlias


def test_set_file_attribute() -> None:
    """Test if file attribute assigned is performed correctly."""
    visitor = StateTrackingVisitor()
    node = TF_FileFunction(
        file_function=FileFunction.Copper,
        fields=["FileFunction", "External"],
    )
    visitor.on_tf_file_function(node)


def test_set_aperture_attribute() -> None:
    """Test if aperture attribute assigned is performed correctly."""
    visitor = StateTrackingVisitor()

    # Test plain assignment of TA_AperFunction
    node = TA_AperFunction(
        function=AperFunction.ViaPad,
        fields=[],
    )
    visitor.on_ta_aper_function(node)
    assert visitor.state.attributes.aperture_attributes[".AperFunction"] == node


def test_set_two_aperture_attribute() -> None:
    """Test if aperture attribute assigned is performed correctly."""
    visitor = StateTrackingVisitor()

    # Test plain assignment of TA_AperFunction
    node0 = TA_AperFunction(
        function=AperFunction.ViaPad,
        fields=[],
    )
    visitor.on_ta_aper_function(node0)
    node1 = TA_DrillTolerance(
        plus_tolerance=0.1,
        minus_tolerance=0.1,
    )
    visitor.on_ta_drill_tolerance(node1)
    assert visitor.state.attributes.aperture_attributes[".AperFunction"] == node0
    assert visitor.state.attributes.aperture_attributes[".DrillTolerance"] == node1


def test_override_aperture_attribute() -> None:
    """Test if overriding aperture attribute is performed correctly."""
    visitor = StateTrackingVisitor()

    # Set initial aperture attribute
    initial_node = TA_AperFunction(
        function=AperFunction.ViaDrill,
        fields=[],
    )
    visitor.on_ta_aper_function(initial_node)

    # Override the aperture attribute
    override_node = TA_AperFunction(
        function=AperFunction.ViaPad,
        fields=[],
    )
    visitor.on_ta_aper_function(override_node)

    # Verify that the attribute has been overridden
    assert (
        visitor.state.attributes.aperture_attributes[".AperFunction"] == override_node
    )


def test_d01_draw_linear_default_quadrant(
    default_d01: D01, mocker: MockerFixture
) -> None:
    """Test if D02 command is handled correctly."""
    on_draw_line = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_draw_line.__name__
    )
    on_draw_cw_arc = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_draw_cw_arc_sq.__name__
    )
    on_draw_ccw_arc = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_draw_ccw_arc_sq.__name__
    )
    visitor = StateTrackingVisitor()

    g_code = G01()
    visitor.on_g01(g_code)
    visitor.on_d01(default_d01)

    on_draw_line.assert_called()
    on_draw_cw_arc.assert_not_called()
    on_draw_ccw_arc.assert_not_called()


@pytest.fixture()
def default_d01() -> D01:
    return _default_d01()


def _default_d01() -> D01:
    return D01(
        x=CoordinateX(value=PackedCoordinateStr("1")),
        y=CoordinateY(value=PackedCoordinateStr("1")),
        i=CoordinateI(value=PackedCoordinateStr("1")),
        j=CoordinateJ(value=PackedCoordinateStr("1")),
    )


def test_d01_draw_cw_arc_default_quadrant(
    default_d01: D01, mocker: MockerFixture
) -> None:
    """Test if D02 command is handled correctly."""
    on_draw_line = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_draw_line.__name__
    )
    on_draw_cw_arc = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_draw_cw_arc_sq.__name__
    )
    on_draw_ccw_arc = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_draw_ccw_arc_sq.__name__
    )
    visitor = StateTrackingVisitor()

    G02().visit(visitor)
    default_d01.visit(visitor)

    on_draw_line.assert_not_called()
    on_draw_cw_arc.assert_called()
    on_draw_ccw_arc.assert_not_called()


def test_d01_draw_ccw_arc_default_quadrant(
    default_d01: D01, mocker: MockerFixture
) -> None:
    """Test if D02 command is handled correctly."""
    on_draw_line = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_draw_line.__name__
    )
    on_draw_cw_arc = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_draw_cw_arc_sq.__name__
    )
    on_draw_ccw_arc = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_draw_ccw_arc_sq.__name__
    )
    visitor = StateTrackingVisitor()

    G03().visit(visitor)
    default_d01.visit(visitor)

    on_draw_line.assert_not_called()
    on_draw_cw_arc.assert_not_called()
    on_draw_ccw_arc.assert_called()


def test_d03_flash_no_aperture(default_d03: D03) -> None:
    """Test if D03 command callbacks are correctly called."""
    visitor = StateTrackingVisitor()

    with pytest.raises(ApertureNotSelectedError):
        visitor.on_d03(default_d03)


def test_d03_flash_circle(default_d03: D03, mocker: MockerFixture) -> None:
    """Test if D03 command callbacks are correctly called."""
    spy = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_flash_circle.__name__
    )
    visitor = StateTrackingVisitor()

    ad = ADC(
        aperture_id=ApertureIdStr("D10"),
        diameter=0.1,
    )
    dnn = Dnn(
        aperture_id=ApertureIdStr("D10"),
    )

    visitor.on_adc(ad)
    visitor.on_dnn(dnn)
    visitor.on_d03(default_d03)

    spy.assert_called_once()


@pytest.fixture()
def default_d03() -> D03:
    return D03(
        x=CoordinateX(value=PackedCoordinateStr("1")),
        y=CoordinateY(value=PackedCoordinateStr("1")),
    )


def test_d03_flash_rectangle(default_d03: D03, mocker: MockerFixture) -> None:
    """Test if D03 command callbacks are correctly called."""
    spy = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_flash_rectangle.__name__
    )
    visitor = StateTrackingVisitor()

    ad = ADR(
        aperture_id=ApertureIdStr("D10"),
        width=0.1,
        height=0.1,
    )
    dnn = Dnn(
        aperture_id=ApertureIdStr("D10"),
    )

    visitor.on_adr(ad)
    visitor.on_dnn(dnn)
    visitor.on_d03(default_d03)

    spy.assert_called_once()


def test_d03_flash_obround(default_d03: D03, mocker: MockerFixture) -> None:
    """Test if D03 command callbacks are correctly called."""
    spy = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_flash_obround.__name__
    )
    visitor = StateTrackingVisitor()

    ad = ADO(
        aperture_id=ApertureIdStr("D10"),
        width=0.1,
        height=0.1,
    )
    dnn = Dnn(
        aperture_id=ApertureIdStr("D10"),
    )

    visitor.on_ado(ad)
    visitor.on_dnn(dnn)
    visitor.on_d03(default_d03)

    spy.assert_called_once()


def test_d03_flash_polygon(default_d03: D03, mocker: MockerFixture) -> None:
    """Test if D03 command callbacks are correctly called."""
    spy = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_flash_polygon.__name__
    )
    visitor = StateTrackingVisitor()

    ad = ADP(
        aperture_id=ApertureIdStr("D10"),
        vertices=6,
        outer_diameter=0.1,
        rotation=0,
        hole_diameter=0.05,
    )
    dnn = Dnn(
        aperture_id=ApertureIdStr("D10"),
    )

    visitor.on_adp(ad)
    visitor.on_dnn(dnn)
    visitor.on_d03(default_d03)

    spy.assert_called_once()


def test_d03_flash_macro(default_d03: D03, mocker: MockerFixture) -> None:
    """Test if D03 command callbacks are correctly called."""
    spy = mocker.spy(StateTrackingVisitor, StateTrackingVisitor.on_flash_macro.__name__)
    visitor = StateTrackingVisitor()

    am = AM(
        open=AMopen(name="MACRO0"),
        primitives=[],
        close=AMclose(),
    )
    ad = ADmacro(
        aperture_id=ApertureIdStr("D10"),
        name="MACRO0",
    )
    dnn = Dnn(
        aperture_id=ApertureIdStr("D10"),
    )

    visitor.on_am(am)
    visitor.on_ad_macro(ad)
    visitor.on_dnn(dnn)
    visitor.on_d03(default_d03)

    spy.assert_called_once()


def test_d03_flash_block(default_d03: D03, mocker: MockerFixture) -> None:
    """Test if D03 command callbacks are correctly called."""
    spy = mocker.spy(StateTrackingVisitor, StateTrackingVisitor.on_flash_block.__name__)
    visitor = StateTrackingVisitor()

    ab = AB(
        open=ABopen(aperture_id=ApertureIdStr("D10")),
        nodes=[],
        close=ABclose(),
    )
    dnn = Dnn(
        aperture_id=ApertureIdStr("D10"),
    )

    visitor.on_ab(ab)
    visitor.on_dnn(dnn)
    visitor.on_d03(default_d03)

    spy.assert_called_once()


def test_switch_to_region_mode_linear_default_quadrant_plot(
    default_d01: D01, mocker: MockerFixture
) -> None:
    """Check if the visitor switches to region mode handlers properly."""
    handler = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_draw_line.__name__
    )
    region_mode_handler = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_in_region_draw_line.__name__
    )
    visitor = StateTrackingVisitor()

    G01().visit(visitor)
    G36().visit(visitor)
    default_d01.visit(visitor)

    handler.assert_not_called()
    region_mode_handler.assert_called()


def test_switch_to_region_mode_arc_default_quadrant_plot(
    default_d01: D01, mocker: MockerFixture
) -> None:
    """Check if the visitor switches to region mode handlers properly."""
    handler = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_draw_cw_arc_sq.__name__
    )
    region_mode_handler = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_in_region_draw_cw_arc_sq.__name__
    )
    visitor = StateTrackingVisitor()

    G02().visit(visitor)
    G36().visit(visitor)
    default_d01.visit(visitor)

    handler.assert_not_called()
    region_mode_handler.assert_called()


def test_switch_to_region_mode_ccw_arc_default_quadrant_plot(
    default_d01: D01, mocker: MockerFixture
) -> None:
    """Check if the visitor switches to region mode handlers properly."""
    handler = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_draw_ccw_arc_sq.__name__
    )
    region_mode_handler = mocker.spy(
        StateTrackingVisitor, StateTrackingVisitor.on_in_region_draw_ccw_arc_sq.__name__
    )
    visitor = StateTrackingVisitor()

    G03().visit(visitor)
    G36().visit(visitor)
    default_d01.visit(visitor)

    handler.assert_not_called()
    region_mode_handler.assert_called()


STATE_TRACKING_VISITOR_D01_CALLBACKS = {
    StateTrackingVisitor.on_draw_line.__name__,
    StateTrackingVisitor.on_draw_cw_arc_sq.__name__,
    StateTrackingVisitor.on_draw_cw_arc_mq.__name__,
    StateTrackingVisitor.on_draw_ccw_arc_sq.__name__,
    StateTrackingVisitor.on_draw_ccw_arc_mq.__name__,
}

STATE_TRACKING_VISITOR_D01_IN_REGION_CALLBACKS = {
    StateTrackingVisitor.on_in_region_draw_line.__name__,
    StateTrackingVisitor.on_in_region_draw_cw_arc_sq.__name__,
    StateTrackingVisitor.on_in_region_draw_cw_arc_mq.__name__,
    StateTrackingVisitor.on_in_region_draw_ccw_arc_sq.__name__,
    StateTrackingVisitor.on_in_region_draw_ccw_arc_mq.__name__,
}
STATE_TRACKING_VISITOR_D01_ALL_CALLBACKS = {
    *STATE_TRACKING_VISITOR_D01_CALLBACKS,
    *STATE_TRACKING_VISITOR_D01_IN_REGION_CALLBACKS,
}

_PARAMS = [
    ([G01(), G37(), G74()], StateTrackingVisitor.on_draw_line.__name__),
    ([G02(), G37(), G74()], StateTrackingVisitor.on_draw_cw_arc_sq.__name__),
    ([G03(), G37(), G74()], StateTrackingVisitor.on_draw_ccw_arc_sq.__name__),
    ([G01(), G36(), G74()], StateTrackingVisitor.on_in_region_draw_line.__name__),
    ([G02(), G36(), G74()], StateTrackingVisitor.on_in_region_draw_cw_arc_sq.__name__),
    ([G03(), G36(), G74()], StateTrackingVisitor.on_in_region_draw_ccw_arc_sq.__name__),
    ([G01(), G37(), G75()], StateTrackingVisitor.on_draw_line.__name__),
    ([G02(), G37(), G75()], StateTrackingVisitor.on_draw_cw_arc_mq.__name__),
    ([G03(), G37(), G75()], StateTrackingVisitor.on_draw_ccw_arc_mq.__name__),
    ([G01(), G36(), G75()], StateTrackingVisitor.on_in_region_draw_line.__name__),
    ([G02(), G36(), G75()], StateTrackingVisitor.on_in_region_draw_cw_arc_mq.__name__),
    ([G03(), G36(), G75()], StateTrackingVisitor.on_in_region_draw_ccw_arc_mq.__name__),
]


@pytest.mark.parametrize(
    ("tokens", "expect"),
    _PARAMS,
)
def test_d01_dispatch(
    tokens: List[Node],
    expect: str,
) -> None:
    """Test if D01 command is dispatched correctly."""
    visitor = StateTrackingVisitor()

    for token in tokens:
        token.visit(visitor)

    assert visitor._on_d01_handler.__name__ == expect


@pytest.mark.parametrize(
    (
        "zeros",
        "coordinate_mode",
        "x_integral",
        "x_decimal",
        "y_integral",
        "y_decimal",
    ),
    [
        (
            Zeros.SKIP_LEADING,
            CoordinateNotation.ABSOLUTE,
            2,
            6,
            3,
            7,
        ),
        (
            Zeros.SKIP_TRAILING,
            CoordinateNotation.ABSOLUTE,
            2,
            6,
            3,
            7,
        ),
        (
            Zeros.SKIP_LEADING,
            CoordinateNotation.INCREMENTAL,
            2,
            6,
            3,
            7,
        ),
        (
            Zeros.SKIP_TRAILING,
            CoordinateNotation.INCREMENTAL,
            2,
            6,
            3,
            7,
        ),
    ],
)
def test_coordinate_format(
    zeros: Zeros,
    coordinate_mode: CoordinateNotation,
    x_integral: int,
    x_decimal: int,
    y_integral: int,
    y_decimal: int,
) -> None:
    node = FS(
        zeros=zeros,
        coordinate_mode=coordinate_mode,
        x_integral=x_integral,
        x_decimal=x_decimal,
        y_integral=y_integral,
        y_decimal=y_decimal,
    )

    visitor = StateTrackingVisitor()
    node.visit(visitor)

    assert visitor.state.coordinate_format == CoordinateFormat(
        zeros=zeros,
        coordinate_mode=coordinate_mode,
        x_integral=x_integral,
        x_decimal=x_decimal,
        y_integral=y_integral,
        y_decimal=y_decimal,
    )


class FMT(CoordinateFormat):
    def __str__(self) -> str:
        return f"{self.zeros.value}{self.coordinate_mode.value}{self.x_integral}{self.x_decimal}{self.y_integral}{self.y_decimal}"

    __repr__ = __str__


ParamsT: TypeAlias = "list[tuple[CoordinateFormat, str, float | type[Exception]]]"


class TestCoordinateFormat:
    fmt_0 = FMT(
        zeros=Zeros.SKIP_LEADING,
        coordinate_mode=CoordinateNotation.ABSOLUTE,
        x_integral=2,
        x_decimal=6,
        y_integral=2,
        y_decimal=6,
    )

    fmt_1 = FMT(
        zeros=Zeros.SKIP_TRAILING,
        coordinate_mode=CoordinateNotation.ABSOLUTE,
        x_integral=2,
        x_decimal=6,
        y_integral=2,
        y_decimal=6,
    )

    params_0: ClassVar[ParamsT] = [
        (fmt_0, "0", 0),
        (fmt_0, "1", 0.000001),
        (fmt_0, "11", 0.000011),
        (fmt_0, "101", 0.000101),
        (fmt_0, "1001", 0.001001),
        (fmt_0, "10001", 0.010001),
        (fmt_0, "100001", 0.100001),
        (fmt_0, "1000001", 1.000001),
        (fmt_0, "10000001", 10.000001),
    ]
    params_1: ClassVar[ParamsT] = [
        (fmt_0, "+0", 0),
        (fmt_0, "+10", 0.00001),
        (fmt_0, "+100", 0.0001),
        (fmt_0, "+1000", 0.001),
        (fmt_0, "+10000", 0.01),
        (fmt_0, "+100000", 0.1),
        (fmt_0, "+1000000", 1),
        (fmt_0, "+10000000", 10),
    ]
    params_2: ClassVar[ParamsT] = [
        (fmt_0, "-10", -0.00001),
        (fmt_0, "-100", -0.0001),
        (fmt_0, "-1000", -0.001),
        (fmt_0, "-10000", -0.01),
        (fmt_0, "-100000", -0.1),
        (fmt_0, "-1000000", -1),
        (fmt_0, "-10000000", -10),
    ]
    params_3: ClassVar[ParamsT] = [
        (fmt_0, "+", PackedCoordinateTooShortError),
        (fmt_0, "+100000000", PackedCoordinateTooLongError),
        (fmt_0, "", PackedCoordinateTooShortError),
        (fmt_0, "100000001", PackedCoordinateTooLongError),
        (fmt_0, "-", PackedCoordinateTooShortError),
        (fmt_0, "-100000000", PackedCoordinateTooLongError),
        (fmt_1, "+1", 10),
        (fmt_1, "-1", -10),
        (fmt_0, "-0", -0),
    ]
    params_4: ClassVar[ParamsT] = [
        (fmt_1, "00000001", 0.000001),
        (fmt_1, "0000001", 0.00001),
        (fmt_1, "000001", 0.0001),
        (fmt_1, "00001", 0.001),
        (fmt_1, "0001", 0.01),
        (fmt_1, "001", 0.1),
        (fmt_1, "01", 1),
        (fmt_1, "1", 10),
    ]
    params_5: ClassVar[ParamsT] = [
        (fmt_1, "10000001", 10.000001),
        (fmt_1, "1000001", 10.00001),
        (fmt_1, "100001", 10.0001),
        (fmt_1, "10001", 10.001),
        (fmt_1, "1001", 10.01),
        (fmt_1, "101", 10.1),
        (fmt_1, "11", 11),
    ]
    params_6: ClassVar[ParamsT] = [
        (fmt_1, "-10000001", -10.000001),
        (fmt_1, "-1000001", -10.00001),
        (fmt_1, "-100001", -10.0001),
        (fmt_1, "-10001", -10.001),
        (fmt_1, "-1001", -10.01),
        (fmt_1, "-101", -10.1),
        (fmt_1, "-11", -11),
    ]

    @pytest.mark.parametrize(
        ("fmt", "input_value", "expected"),
        [
            *params_0,
            *params_1,
            *params_2,
            *params_3,
            *params_4,
            *params_5,
            *params_6,
        ],
        ids=lambda x: x.__qualname__ if isclass(x) else str(x),
    )
    def test_unpack_x(
        self,
        fmt: CoordinateFormat,
        input_value: PackedCoordinateStr,
        expected: float | type[Exception],
    ) -> None:
        """Test if x coordinate is unpacked correctly."""
        if not isinstance(expected, (int, float)):
            with pytest.raises(expected):
                fmt.unpack_x(input_value)
        else:
            assert fmt.unpack_x(input_value) == expected

    @pytest.mark.parametrize(
        ("fmt", "input_value", "expected"),
        [
            *params_0,
            *params_1,
            *params_2,
            *params_3,
            *params_4,
            *params_5,
            *params_6,
        ],
        ids=lambda x: x.__qualname__ if isclass(x) else str(x),
    )
    def test_unpack_y(
        self,
        fmt: CoordinateFormat,
        input_value: PackedCoordinateStr,
        expected: float | type[Exception],
    ) -> None:
        """Test if y coordinate is unpacked correctly."""
        if not isinstance(expected, (int, float)):
            with pytest.raises(expected):
                fmt.unpack_y(input_value)
        else:
            assert fmt.unpack_y(input_value) == expected

    @pytest.mark.parametrize(
        ("fmt", "expected", "input_value"),
        [
            *params_0,
            # *params_1,
            *params_2,
            # *params_3,
            *params_4,
            *params_5,
            *params_6,
        ],
        ids=lambda x: x.__qualname__ if isclass(x) else str(x),
    )
    def test_pack_x(
        self,
        fmt: CoordinateFormat,
        expected: PackedCoordinateStr,
        input_value: float | type[Exception],
    ) -> None:
        """Test if x coordinate is unpacked correctly."""
        if not isinstance(input_value, (int, float)):
            pytest.skip()
        else:
            assert fmt.pack_x(input_value) == expected
