from __future__ import annotations

from unittest.mock import MagicMock

from pygerber.gerberx3.ast.nodes import (
    D01,
    G01,
    G02,
    G03,
    CoordinateI,
    CoordinateJ,
    CoordinateX,
    CoordinateY,
    PackedCoordinateStr,
    TA_AperFunction,
    TA_DrillTolerance,
    TF_FileFunction,
)
from pygerber.gerberx3.ast.nodes.enums import AperFunction, FileFunction
from pygerber.gerberx3.ast.state_tracking_visitor import StateTrackingVisitor


def test_set_file_attribute() -> None:
    """Test if file attribute assigned is performed correctly."""
    visitor = StateTrackingVisitor()
    node = TF_FileFunction(
        source="",
        location=0,
        file_function=FileFunction.Copper,
        fields=["FileFunction", "External"],
    )
    visitor.on_tf_file_function(node)


def test_set_aperture_attribute() -> None:
    """Test if aperture attribute assigned is performed correctly."""
    visitor = StateTrackingVisitor()

    # Test plain assignment of TA_AperFunction
    node = TA_AperFunction(
        source="",
        location=0,
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
        source="",
        location=0,
        function=AperFunction.ViaPad,
        fields=[],
    )
    visitor.on_ta_aper_function(node0)
    node1 = TA_DrillTolerance(
        source="",
        location=0,
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
        source="",
        location=0,
        function=AperFunction.ViaDrill,
        fields=[],
    )
    visitor.on_ta_aper_function(initial_node)

    # Override the aperture attribute
    override_node = TA_AperFunction(
        source="",
        location=0,
        function=AperFunction.ViaPad,
        fields=[],
    )
    visitor.on_ta_aper_function(override_node)

    # Verify that the attribute has been overridden
    assert (
        visitor.state.attributes.aperture_attributes[".AperFunction"] == override_node
    )


def test_d02_draw_linear() -> None:
    """Test if D02 command is handled correctly."""
    visitor = StateTrackingVisitor()
    visitor.on_draw_line = MagicMock()  # type: ignore[method-assign]
    visitor.on_draw_cw_arc = MagicMock()  # type: ignore[method-assign]
    visitor.on_draw_ccw_arc = MagicMock()  # type: ignore[method-assign]

    d_code = D01(
        source="",
        location=0,
        x=CoordinateX(source="", location=0, value=PackedCoordinateStr("1")),
        y=CoordinateY(source="", location=0, value=PackedCoordinateStr("1")),
    )
    g_code = G01(
        source="",
        location=0,
    )
    visitor.on_g01(g_code)
    visitor.on_d01(d_code)

    assert visitor.on_draw_line.called
    assert not visitor.on_draw_cw_arc.called
    assert not visitor.on_draw_ccw_arc.called


def test_d02_draw_cw_arc() -> None:
    """Test if D02 command is handled correctly."""
    visitor = StateTrackingVisitor()
    visitor.on_draw_line = MagicMock()  # type: ignore[method-assign]
    visitor.on_draw_cw_arc = MagicMock()  # type: ignore[method-assign]
    visitor.on_draw_ccw_arc = MagicMock()  # type: ignore[method-assign]

    d_code = D01(
        source="",
        location=0,
        x=CoordinateX(source="", location=0, value=PackedCoordinateStr("1")),
        y=CoordinateY(source="", location=0, value=PackedCoordinateStr("1")),
        i=CoordinateI(source="", location=0, value=PackedCoordinateStr("1")),
        j=CoordinateJ(source="", location=0, value=PackedCoordinateStr("1")),
    )
    g_code = G02(
        source="",
        location=0,
    )
    visitor.on_g02(g_code)
    visitor.on_d01(d_code)

    assert not visitor.on_draw_line.called
    assert visitor.on_draw_cw_arc.called
    assert not visitor.on_draw_ccw_arc.called


def test_d02_draw_ccw_arc() -> None:
    """Test if D02 command is handled correctly."""
    visitor = StateTrackingVisitor()
    visitor.on_draw_line = MagicMock()  # type: ignore[method-assign]
    visitor.on_draw_cw_arc = MagicMock()  # type: ignore[method-assign]
    visitor.on_draw_ccw_arc = MagicMock()  # type: ignore[method-assign]

    d_code = D01(
        source="",
        location=0,
        x=CoordinateX(source="", location=0, value=PackedCoordinateStr("1")),
        y=CoordinateY(source="", location=0, value=PackedCoordinateStr("1")),
        i=CoordinateI(source="", location=0, value=PackedCoordinateStr("1")),
        j=CoordinateJ(source="", location=0, value=PackedCoordinateStr("1")),
    )
    g_code = G03(
        source="",
        location=0,
    )
    visitor.on_g03(g_code)
    visitor.on_d01(d_code)

    assert not visitor.on_draw_line.called
    assert not visitor.on_draw_cw_arc.called
    assert visitor.on_draw_ccw_arc.called
