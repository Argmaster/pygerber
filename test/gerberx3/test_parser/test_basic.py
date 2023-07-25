"""Tokenizer tests based on A64-OLinuXino-rev-G board."""

from __future__ import annotations
from decimal import Decimal

from typing import TYPE_CHECKING

import pytest

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


def test_source_0(asset_loader: AssetLoader) -> None:
    """Parser test based on source.grb file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/basic/sample-0/source.grb").decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()

    assert parser.state.coordinate_parser is not None
    assert parser.state.coordinate_parser.x_format == AxisFormat(integer=2, decimal=6)
    assert parser.state.coordinate_parser.y_format == AxisFormat(integer=2, decimal=6)

    assert parser.state.coordinate_parser.parse(
        Coordinate(
            coordinate_type=CoordinateType.X,
            sign=CoordinateSign.Positive,
            offset="1100010",
        )
    ) == Decimal("1.100010")

    assert parser.state.coordinate_parser.parse(
        Coordinate(
            coordinate_type=CoordinateType.X,
            sign=CoordinateSign.Positive,
            offset="500",
        )
    ) == Decimal("0.000500")

    assert parser.state.draw_units == Unit.Millimeters


def test_source_1(asset_loader: AssetLoader) -> None:
    """Parser test based on source.grb file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/basic/sample-1/source.grb").decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


def test_source_2(asset_loader: AssetLoader) -> None:
    """Parser test based on source.grb file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/basic/sample-2/source.grb").decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


def test_source_3(asset_loader: AssetLoader) -> None:
    """Parser test based on source.grb file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/basic/sample-3/source.grb").decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


def test_source_4(asset_loader: AssetLoader) -> None:
    """Parser test based on source.grb file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/basic/sample-4/source.grb").decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


# TODO(argmaster.world@gmail.com): Add support for block apertures.
# https://github.com/Argmaster/pygerber/issues/24
@pytest.mark.xfail(reason="Parser is lacking support for block apertures.")
def test_source_5(asset_loader: AssetLoader) -> None:
    """Parser test based on source.grb file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/basic/sample-5/source.grb").decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()
