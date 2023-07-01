#!/usr/bin/env python

"""Standalone script for installing hooks from `scripts/hooks` directory into git
repository.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import click

THIS_FILE = Path(__file__)
THIS_FILE_DIRECTORY = THIS_FILE.parent
REPOSITORY_ROOT_DIRECTORY = THIS_FILE_DIRECTORY.parent
REPOSITORY_HOOKS_DIRECTORY = REPOSITORY_ROOT_DIRECTORY / ".git" / "hooks"


@click.command()
def main() -> None:
    """Install hooks from `scripts/hooks` directory into git repository."""
    for file in (THIS_FILE_DIRECTORY / "hooks").rglob("*"):
        shutil.copy(file.as_posix(), REPOSITORY_HOOKS_DIRECTORY.as_posix())


if __name__ == "__main__":
    main()
