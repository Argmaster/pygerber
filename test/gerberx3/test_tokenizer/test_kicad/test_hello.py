"""Tokenizer tests based on Kicad hello."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def test_tokenizer_sample_b_cu(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample B_Cu.gbr."""
    Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/kicad/hello/B_Cu/B_Cu.gbr").decode(
            "utf-8",
        ),
    )


def test_tokenizer_sample_edge_cuts(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample Edge_Cuts.gbr."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/kicad/hello/Edge_Cuts/Edge_Cuts.gbr",
        ).decode("utf-8"),
    )


def test_tokenizer_sample_f_cu(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample F_Cu.gbr."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/kicad/hello/F_Cu/F_Cu.gbr",
        ).decode("utf-8"),
    )


def test_tokenizer_sample_f_mask(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample F_Mask.gbr."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/kicad/hello/F_Mask/F_Mask.gbr",
        ).decode("utf-8"),
    )


def test_tokenizer_sample_f_paste(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample F_Paste.gbr."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/kicad/hello/F_Paste/F_Paste.gbr",
        ).decode("utf-8"),
    )


def test_tokenizer_sample_f_silkscreen(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample F_Silkscreen.gbr."""
    Tokenizer().tokenize(
        asset_loader.load_asset(
            "gerberx3/kicad/hello/F_Silkscreen/F_Silkscreen.gbr",
        ).decode("utf-8"),
    ).debug_display()
