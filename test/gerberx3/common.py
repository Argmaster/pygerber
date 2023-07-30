"""Common utilities for gerber tests."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from pygerber.gerberx3.tokenizer.tokenizer import TokenStack, Tokenizer
from test.conftest import AssetLoader


def find_gerberx3_asset_files(directory: str | Path) -> Iterable[tuple[str, str]]:
    directory_to_inspect = Path.cwd() / directory
    for path in sorted(directory_to_inspect.resolve().rglob("*.g??")):
        path = path.relative_to(directory_to_inspect.parent)
        yield path.parent.as_posix(), path.name


def tokenize_gerberx3(
    asset_loader: AssetLoader, directory: Path, file_name: str
) -> TokenStack:
    return Tokenizer().tokenize(
        asset_loader.load_asset(f"gerberx3/{directory}/{file_name}").decode(
            "utf-8",
        ),
    )


def save_token_stack(
    stack: TokenStack, test_file_path: str, directory: Path, file_name: str
) -> None:
    output_directory = Path(test_file_path).parent / ".output" / directory
    output_directory.mkdir(0o777, parents=True, exist_ok=True)
    token_file_path = (output_directory / file_name).with_suffix(".txt")
    content = stack.format_gerberx3()
    token_file_path.touch(0o777, exist_ok=True)
    token_file_path.write_text(content)
