"""Common utilities for gerber tests."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Iterable

from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer, TokenStack

if TYPE_CHECKING:
    from test.conftest import AssetLoader

ASSET_PATH_BASE = "test/assets/gerberx3"


def find_gerberx3_asset_files(directory: str | Path) -> Iterable[tuple[str, str]]:
    directory_to_inspect = Path.cwd() / directory
    asset_path_base = Path.cwd() / ASSET_PATH_BASE

    for path in sorted(directory_to_inspect.resolve().rglob("*.g??")):
        relative_path = path.relative_to(asset_path_base)
        yield relative_path.parent.as_posix(), relative_path.name


def tokenize_gerberx3(
    asset_loader: AssetLoader,
    directory: Path,
    file_name: str,
    *,
    only_expressions: bool = False,
) -> TokenStack:
    string = asset_loader.load_asset(f"gerberx3/{directory}/{file_name}").decode(
        "utf-8",
    )
    if only_expressions:
        return Tokenizer().tokenize_expressions(string)

    return Tokenizer().tokenize(string)


def save_token_stack(
    stack: TokenStack,
    test_file_path: str,
    directory: Path,
    file_name: str,
) -> None:
    output_directory = Path(test_file_path).parent / ".output" / directory
    output_directory.mkdir(0o777, parents=True, exist_ok=True)
    token_file_path = (output_directory / file_name).with_suffix(".txt")
    content = stack.format_gerberx3()
    token_file_path.touch(0o777, exist_ok=True)
    token_file_path.write_text(content)
