"""Test AM (Aperture Macro) definition tokenization."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def test_tokenizer_sample_am_sample_0(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample 0."""
    Tokenizer().tokenize_expressions(
        asset_loader.load_asset(
            "gerberx3/expressions/AM/sample-0.gbr",
        ).decode("utf-8"),
    ).debug_display()


def test_tokenizer_sample_am_sample_0b(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample 0b, with 'X' for multiplication."""
    Tokenizer().tokenize_expressions(
        asset_loader.load_asset("gerberx3/expressions/AM/sample-0b.gbr").decode(
            "utf-8",
        ),
    ).debug_display()


def test_tokenizer_sample_am_sample_1(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample 1."""
    Tokenizer().tokenize_expressions(
        asset_loader.load_asset(
            "gerberx3/expressions/AM/sample-1.gbr",
        ).decode("utf-8"),
    ).debug_display()


def test_tokenizer_sample_am_sample_2(asset_loader: AssetLoader) -> None:
    """Test tokenizer on sample 2."""
    Tokenizer().tokenize_expressions(
        asset_loader.load_asset(
            "gerberx3/expressions/AM/sample-2.gbr",
        ).decode("utf-8"),
    ).debug_display()
