"""Global test configuration."""

from __future__ import annotations

import datetime
import json
import logging
import logging.handlers
import os
from contextlib import contextmanager, suppress
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Generator

import pytest
import tzlocal

THIS_FILE = Path(__file__)
THIS_FILE_DIRECTORY = THIS_FILE.parent
TEST_DIRECTORY = THIS_FILE_DIRECTORY
ASSETS_DIRECTORY = TEST_DIRECTORY / "assets"


@contextmanager
def cd_to_tempdir() -> Generator[Path, None, None]:
    original_cwd = Path.cwd().as_posix()
    tempdir = TemporaryDirectory()
    os.chdir(tempdir.name)
    try:
        yield Path(tempdir.name)
    finally:
        os.chdir(original_cwd)
        with suppress(
            FileNotFoundError, NotADirectoryError, FileExistsError, PermissionError
        ):
            tempdir.cleanup()


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

    def load_asset_overrides(self, src: str) -> dict[str, Any]:
        src = f"{src}.overrides"
        asset = self.asset_cache.get(src)
        if asset is None:
            try:
                asset = self._load_asset(src)
            except FileNotFoundError:
                asset = b"{}"

        config = json.loads(asset)
        assert isinstance(config, dict)
        return config

    def _load_asset(self, src: str) -> bytes:
        return (self.assets_directory / src).read_bytes()


GLOBAL_ASSET_LOADER = AssetLoader(ASSETS_DIRECTORY)


@pytest.fixture
def asset_loader() -> AssetLoader:
    """Acquire global asset loader."""
    return GLOBAL_ASSET_LOADER


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

start_time = datetime.datetime.now(tz=tzlocal.get_localzone())
log_file_path = Path.cwd() / "log" / "test" / "pygerber_pytest.log"
log_file_path.parent.mkdir(0o777, parents=True, exist_ok=True)
file_handler = logging.handlers.RotatingFileHandler(
    log_file_path.as_posix(),
    encoding="utf-8",
    backupCount=16,
    maxBytes=16 * 1024**2,  # Max 16 MB
)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


logging.debug("Configured logger at %s", start_time.isoformat())
