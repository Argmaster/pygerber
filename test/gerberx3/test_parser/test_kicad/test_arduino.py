"""Tokenizer tests based on Kicad arduino template."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

from pygerber.gerberx3.parser.parser import Parser

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def test_User_Drawings(asset_loader: AssetLoader) -> None:  # noqa: N802
    """Parser test based on User_Drawings file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/arduino/User_Drawings.gbr").decode(
            "utf-8"
        ),
    )

    parser = Parser()
    parser.parse(stack)


def test_B_Cu(asset_loader: AssetLoader) -> None:  # noqa: N802
    """Parser test based on B_Cu file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/arduino/B_Cu.gbr").decode("utf-8"),
    )

    parser = Parser()
    parser.parse(stack)


def test_F_Cu(asset_loader: AssetLoader) -> None:  # noqa: N802
    """Parser test based on F_Cu file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/arduino/F_Cu.gbr").decode("utf-8"),
    )

    parser = Parser()
    parser.parse(stack)


def test_F_Silkscreen(asset_loader: AssetLoader) -> None:  # noqa: N802
    """Parser test based on F_Silkscreen file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/arduino/F_Silkscreen.gbr").decode(
            "utf-8"
        ),
    )

    parser = Parser()
    parser.parse(stack)


def test_F_Mask(asset_loader: AssetLoader) -> None:  # noqa: N802
    """Parser test based on F_Mask file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/arduino/F_Mask.gbr").decode("utf-8"),
    )

    parser = Parser()
    parser.parse(stack)
