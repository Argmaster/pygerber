from __future__ import annotations

from pathlib import Path

import pytest

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


@pytest.mark.parametrize(
    "example_path",
    [
        *THIS_DIRECTORY.glob("*.example.py"),
    ],
    ids=lambda path: path.name,
)
def test_examples(example_path: Path) -> None:
    exec(example_path.read_text(encoding="utf-8"))  # noqa: S102
