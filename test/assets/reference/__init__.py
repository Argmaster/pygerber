from __future__ import annotations

from pathlib import Path

from test.assets.assetlib import GitRepository

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


REFERENCE_REPOSITORY = GitRepository.new_remote(
    "https://github.com/PyGerber/pygerber_reference_assets", "main"
).init()
