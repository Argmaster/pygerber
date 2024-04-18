"""tests based on basic examples."""

from __future__ import annotations

from decimal import Decimal
from test.gerberx3.test_parser.common import make_parser_test
from typing import TYPE_CHECKING

from pygerber.gerberx3.parser.parser import Parser
from pygerber.gerberx3.state_enums import Unit
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer
from pygerber.gerberx3.tokenizer.tokens.coordinate import (
    Coordinate,
    CoordinateSign,
    CoordinateType,
)
from pygerber.gerberx3.tokenizer.tokens.fs_coordinate_format import AxisFormat

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def test_manual_comparison(asset_loader: AssetLoader) -> None:
    """Parser test based on source.grb file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/basic/sample-0/source.grb").decode("utf-8"),
    )

    parser = Parser()
    parser.parse(stack)

    assert parser.state.coordinate_parser is not None
    assert parser.state.coordinate_parser.x_format == AxisFormat(integer=2, decimal=6)
    assert parser.state.coordinate_parser.y_format == AxisFormat(integer=2, decimal=6)

    assert parser.state.coordinate_parser.parse(
        Coordinate(
            coordinate_type=CoordinateType.X,
            sign=CoordinateSign.Positive,
            offset="1100010",
        ),
    ) == Decimal("1.100010")

    assert parser.state.coordinate_parser.parse(
        Coordinate(
            coordinate_type=CoordinateType.X,
            sign=CoordinateSign.Positive,
            offset="500",
        ),
    ) == Decimal("0.000500")

    assert parser.state.draw_units == Unit.Millimeters


test_sample = make_parser_test(__file__, "test/assets/gerberx3/basic")
