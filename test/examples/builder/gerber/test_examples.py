from __future__ import annotations

from pathlib import Path

import pytest

from test.conftest import cd_to_tempdir

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


@pytest.mark.parametrize(
    "example_path",
    [
        *THIS_DIRECTORY.glob("*.ex.py"),
    ],
    ids=lambda path: path.name,
)
def test_example(example_path: Path) -> None:
    with cd_to_tempdir():
        exec(example_path.read_text(encoding="utf-8"))  # noqa: S102
