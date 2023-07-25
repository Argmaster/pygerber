"""Tokenizer tests based on ATMEGA328-Motor-Board project."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest


from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

from pygerber.gerberx3.parser.parser import Parser

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def test_ATMEGA328_Motor_Board_B_Cu(
    asset_loader: AssetLoader,
) -> None:
    """Parser test based on ATMEGA328_Motor_Board-B.Cu file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-B.Cu.gbl"
        ).decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


def test_ATMEGA328_Motor_Board_B_Mask(
    asset_loader: AssetLoader,
) -> None:
    """Parser test based on ATMEGA328_Motor_Board-B.Mask file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-B.Mask.gbs"
        ).decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


def test_ATMEGA328_Motor_Board_F_Mask(
    asset_loader: AssetLoader,
) -> None:
    """Parser test based on ATMEGA328_Motor_Board-F.Mask file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-F.Mask.gts"
        ).decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


def test_ATMEGA328_Motor_Board_F_Cu(
    asset_loader: AssetLoader,
) -> None:
    """Parser test based on ATMEGA328_Motor_Board-F.Cu file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-F.Cu.gtl"
        ).decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


@pytest.mark.xfail(reason="No support for G0X merged with D01")
def test_ATMEGA328_Motor_Board_F_SilkS(
    asset_loader: AssetLoader,
) -> None:
    """Parser test based on ATMEGA328_Motor_Board-F.SilkS file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-F.SilkS.gto"
        ).decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


def test_ATMEGA328_Motor_Board_F_Paste(
    asset_loader: AssetLoader,
) -> None:
    """Parser test based on ATMEGA328_Motor_Board-F.Paste file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-F.Paste.gtp"
        ).decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


def test_ATMEGA328_Motor_Board_Edge_Cuts(
    asset_loader: AssetLoader,
) -> None:
    """Parser test based on ATMEGA328_Motor_Board-Edge.Cuts file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-Edge.Cuts.gm1"
        ).decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


def test_ATMEGA328_Motor_Board_B_Paste(
    asset_loader: AssetLoader,
) -> None:
    """Parser test based on ATMEGA328_Motor_Board-B.Paste file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-B.Paste.gbp"
        ).decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()


def test_ATMEGA328_Motor_Board_B_SilkS(
    asset_loader: AssetLoader,
) -> None:
    """Parser test based on ATMEGA328_Motor_Board-B.SilkS file."""
    stack = Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-B.SilkS.gbo"
        ).decode("utf-8"),
    )

    parser = Parser(stack)
    parser.parse()
