"""Global test configuration."""

from __future__ import annotations

from pathlib import Path

import pytest

THIS_FILE = Path(__file__)
THIS_FILE_DIRECTORY = THIS_FILE.parent
TEST_DIRECTORY = THIS_FILE_DIRECTORY
ASSETS_DIRECTORY = TEST_DIRECTORY / "assets"


class AssetLoader:
    """Loader class for simplified asset loading from files."""

    asset_cache: dict[str, bytes]

    def __init__(self, assets_directory: Path) -> None:
        """Initialize asset loader."""
        self.assets_directory = assets_directory
        self.asset_cache = {}

    def load_asset(self, src: str) -> bytes:
        """Load asset from location in assets directory."""
        asset = self.asset_cache.get(src)
        if asset is None:
            asset = self._load_asset(src)

        return asset

    def _load_asset(self, src: str) -> bytes:
        return (self.assets_directory / src).read_bytes()


GLOBAL_ASSET_LOADER = AssetLoader(ASSETS_DIRECTORY)


@pytest.fixture()
def asset_loader() -> AssetLoader:
    """Acquire global asset loader."""
    return GLOBAL_ASSET_LOADER
