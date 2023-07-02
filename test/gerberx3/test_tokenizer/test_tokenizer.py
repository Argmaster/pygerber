"""Test tokenizer class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def test_tokenizer_sample_0(asset_loader: AssetLoader) -> None:
    """Test tokenizer of sample 0."""
    Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/basic/sample-0/source.grb").decode("utf-8"),
    )


def test_tokenizer_sample_1(asset_loader: AssetLoader) -> None:
    """Test tokenizer of sample 1."""
    Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/basic/sample-1/source.grb").decode("utf-8"),
    )


def test_tokenizer_sample_2(asset_loader: AssetLoader) -> None:
    """Test tokenizer of sample 2."""
    Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/basic/sample-2/source.grb").decode("utf-8"),
    )


def test_tokenizer_sample_3(asset_loader: AssetLoader) -> None:
    """Test tokenizer of sample 3."""
    Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/basic/sample-3/source.grb").decode("utf-8"),
    )


def test_tokenizer_sample_4(asset_loader: AssetLoader) -> None:
    """Test tokenizer of sample 4."""
    Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/basic/sample-4/source.grb").decode("utf-8"),
    )
