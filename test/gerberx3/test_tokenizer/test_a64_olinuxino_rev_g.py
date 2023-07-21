"""Tokenizer tests based on A64-OLinuXino-rev-G board."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def test_tokenizer_A64_OlinuXino_Rev_G_B_Mask(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on A64-OlinuXino_Rev_G-B_Mask file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/A64-OLinuXino-rev-G/A64-OlinuXino_Rev_G-B_Mask.gbr",
        ).decode("utf-8"),
    )


def test_tokenizer_A64_OlinuXino_Rev_G_In3_Cu(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on A64-OlinuXino_Rev_G-In3_Cu file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/A64-OLinuXino-rev-G/A64-OlinuXino_Rev_G-In3_Cu.gbr",
        ).decode("utf-8"),
    )


def test_tokenizer_A64_OlinuXino_Rev_G_In1_Cu(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on A64-OlinuXino_Rev_G-In1_Cu file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/A64-OLinuXino-rev-G/A64-OlinuXino_Rev_G-In1_Cu.gbr",
        ).decode("utf-8"),
    )


def test_tokenizer_A64_OlinuXino_Rev_G_In4_Cu(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on A64-OlinuXino_Rev_G-In4_Cu file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/A64-OLinuXino-rev-G/A64-OlinuXino_Rev_G-In4_Cu.gbr",
        ).decode("utf-8"),
    )


def test_tokenizer_A64_OlinuXino_Rev_G_F_Paste(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on A64-OlinuXino_Rev_G-F_Paste file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/A64-OLinuXino-rev-G/A64-OlinuXino_Rev_G-F_Paste.gbr",
        ).decode("utf-8"),
    )


def test_tokenizer_A64_OlinuXino_Rev_G_B_Paste(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on A64-OlinuXino_Rev_G-B_Paste file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/A64-OLinuXino-rev-G/A64-OlinuXino_Rev_G-B_Paste.gbr",
        ).decode("utf-8"),
    )


def test_tokenizer_A64_OlinuXino_Rev_G_B_Cu(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on A64-OlinuXino_Rev_G-B_Cu file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/A64-OLinuXino-rev-G/A64-OlinuXino_Rev_G-B_Cu.gbr",
        ).decode("utf-8"),
    )


def test_tokenizer_A64_OlinuXino_Rev_G_Edge_Cuts(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on A64-OlinuXino_Rev_G-Edge_Cuts file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/A64-OLinuXino-rev-G/A64-OlinuXino_Rev_G-Edge_Cuts.gbr",
        ).decode("utf-8"),
    )


def test_tokenizer_A64_OlinuXino_Rev_G_F_Cu(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on A64-OlinuXino_Rev_G-F_Cu file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/A64-OLinuXino-rev-G/A64-OlinuXino_Rev_G-F_Cu.gbr",
        ).decode("utf-8"),
    )


@pytest.mark.xfail(reason="No support for G0X merged with D01")
def test_tokenizer_A64_OlinuXino_Rev_G_F_SilkS(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on A64-OlinuXino_Rev_G-F_SilkS file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/A64-OLinuXino-rev-G/A64-OlinuXino_Rev_G-F_SilkS.gbr",
        ).decode("utf-8"),
    )


@pytest.mark.xfail(reason="No support for G0X merged with D01")
def test_tokenizer_A64_OlinuXino_Rev_G_B_SilkS(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on A64-OlinuXino_Rev_G-B_SilkS file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/A64-OLinuXino-rev-G/A64-OlinuXino_Rev_G-B_SilkS.gbr",
        ).decode("utf-8"),
    )


def test_tokenizer_A64_OlinuXino_Rev_G_In2_Cu(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on A64-OlinuXino_Rev_G-In2_Cu file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/A64-OLinuXino-rev-G/A64-OlinuXino_Rev_G-In2_Cu.gbr",
        ).decode("utf-8"),
    )


def test_tokenizer_A64_OlinuXino_Rev_G_F_Mask(  # noqa: N802
    asset_loader: AssetLoader,
) -> None:
    """Tokenizer test based on A64-OlinuXino_Rev_G-F_Mask file."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/A64-OLinuXino-rev-G/A64-OlinuXino_Rev_G-F_Mask.gbr",
        ).decode("utf-8"),
    )
