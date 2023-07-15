"""Tokenizer tests based on Kicad arduino template."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def test_tokenizer_sample_b_cu(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample B_Cu.gbr."""
    Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/arduino/B_Cu.gbr").decode("utf-8"),
    )


def test_tokenizer_sample_f_cu(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample F_Cu.gbr."""
    Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/arduino/F_Cu.gbr").decode("utf-8"),
    )


def test_tokenizer_sample_f_mask(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample F_Mask.gbr."""
    Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/arduino/F_Mask.gbr").decode(
            "utf-8",
        ),
    )


def test_tokenizer_sample_f_silkscreen(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample F_Silkscreen.gbr."""
    Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/arduino/F_Silkscreen.gbr").decode(
            "utf-8",
        ),
    )


def test_tokenizer_sample_user_drawings(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample User_Drawings.gbr."""
    Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/arduino/User_Drawings.gbr").decode(
            "utf-8",
        ),
    )
