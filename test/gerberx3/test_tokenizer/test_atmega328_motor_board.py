"""Tokenizer tests based on A64-OLinuXino-rev-G board."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def test_tokenizer_ATMEGA328_Motor_Board_B_Cu(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on ATMEGA328_Motor_Board-B.Cu file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-B.Cu.gbl",
        ).decode("utf-8"),
    )


def test_tokenizer_ATMEGA328_Motor_Board_B_Mask(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on ATMEGA328_Motor_Board-B.Mask file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-B.Mask.gbs",
        ).decode("utf-8"),
    )


def test_tokenizer_ATMEGA328_Motor_Board_F_Mask(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on ATMEGA328_Motor_Board-F.Mask file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-F.Mask.gts",
        ).decode("utf-8"),
    )


def test_tokenizer_ATMEGA328_Motor_Board_F_Cu(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on ATMEGA328_Motor_Board-F.Cu file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-F.Cu.gtl",
        ).decode("utf-8"),
    )


@pytest.mark.xfail(reason="No support for G0X merged with D01")
def test_tokenizer_ATMEGA328_Motor_Board_F_SilkS(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on ATMEGA328_Motor_Board-F.SilkS file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-F.SilkS.gto",
        ).decode("utf-8"),
    )


def test_tokenizer_ATMEGA328_Motor_Board_F_Paste(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on ATMEGA328_Motor_Board-F.Paste file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-F.Paste.gtp",
        ).decode("utf-8"),
    )


def test_tokenizer_ATMEGA328_Motor_Board_Edge_Cuts(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on ATMEGA328_Motor_Board-Edge.Cuts file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-Edge.Cuts.gm1",
        ).decode("utf-8"),
    )


def test_tokenizer_ATMEGA328_Motor_Board_B_Paste(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on ATMEGA328_Motor_Board-B.Paste file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-B.Paste.gbp",
        ).decode("utf-8"),
    )


def test_tokenizer_ATMEGA328_Motor_Board_B_SilkS(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on ATMEGA328_Motor_Board-B.SilkS file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-B.SilkS.gbo",
        ).decode("utf-8"),
    )
