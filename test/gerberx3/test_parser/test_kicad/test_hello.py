"""Tokenizer tests based on Kicad arduino template."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

from pygerber.gerberx3.parser.parser import Parser

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def test_parser_F_Cu(asset_loader: AssetLoader) -> None:  # noqa: N802
    """Parser test based on F_Cu file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/hello/F_Cu/F_Cu.gbr").decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


def test_parser_B_Cu(asset_loader: AssetLoader) -> None:  # noqa: N802
    """Parser test based on B_Cu file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/hello/B_Cu/B_Cu.gbr").decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


def test_parser_F_Paste(asset_loader: AssetLoader) -> None:  # noqa: N802
    """Parser test based on F_Paste file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/hello/F_Paste/F_Paste.gbr").decode(
            "utf-8"
        ),
    )

    parser = Parser(stack)
    parser.parse()


def test_parser_F_Silkscreen(asset_loader: AssetLoader) -> None:  # noqa: N802
    """Parser test based on F_Silkscreen file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/kicad/hello/F_Silkscreen/F_Silkscreen.gbr"
        ).decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


def test_parser_F_Mask(asset_loader: AssetLoader) -> None:  # noqa: N802
    """Parser test based on F_Mask file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/hello/F_Mask/F_Mask.gbr").decode(
            "utf-8"
        ),
    )

    parser = Parser(stack)
    parser.parse()


def test_parser_Edge_Cuts(asset_loader: AssetLoader) -> None:  # noqa: N802
    """Parser test based on Edge_Cuts file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/hello/Edge_Cuts/Edge_Cuts.gbr").decode(
            "utf-8"
        ),
    )

    parser = Parser(stack)
    parser.parse()
