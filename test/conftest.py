"""Global test configuration."""

from __future__ import annotations

import datetime
import logging
from pathlib import Path

import pytest
import tzlocal

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


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

start_time = datetime.datetime.now(tz=tzlocal.get_localzone())
log_file_path = (
    Path.cwd() / "log" / "test" / f"{start_time.isoformat(timespec='hours')}.log"
)
log_file_path.parent.mkdir(0o777, parents=True, exist_ok=True)
file_handler = logging.FileHandler(log_file_path.as_posix(), encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


logging.debug("Configured logger at %s", start_time.isoformat())
