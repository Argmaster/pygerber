"""Common utilities for gerber tests."""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generator,
    Generic,
    Iterable,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
)

import pytest
from PIL import Image, ImageDraw

from pygerber.gerber.api._enums import GERBER_EXTENSION_TO_FILE_TYPE_MAPPING
from test.assets.reference.pygerber.console import THIS_DIRECTORY as ASSETS_DIRECTORY

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

ASSET_PATH_BASE = "test/assets/gerberx3"


def find_gerberx3_asset_files(directory: str | Path) -> Iterable[tuple[str, str]]:
    directory_to_inspect = Path.cwd() / directory
    asset_path_base = Path.cwd() / ASSET_PATH_BASE

    for path in sorted(directory_to_inspect.resolve().rglob("*.g??")):
        relative_path = path.relative_to(asset_path_base)
        yield relative_path.parent.as_posix(), relative_path.name


GERBER_ASSETS_DIRECTORY = ASSETS_DIRECTORY / "gerberx3"
REFERENCE_ASSETS_HASH = ""


class AssetLoader2:
    def __init__(self, assets_directory: Path) -> None:
        """Initialize asset loader."""
        self.assets_directory = assets_directory
        self.assets_cache: dict[str, Any] = {}
        self.assets_index: dict[Path, Asset] = {}

    def detect_assets(self) -> None:
        self.assets_index = {
            p.expanduser().resolve(): Asset(
                self.assets_directory,
                p.expanduser().resolve(),
                p.relative_to(self.assets_directory),
            )
            for p in self.assets_directory.rglob("*.*")
        }

    def iter_assets(
        self, extensions: Optional[Sequence[str]] = None
    ) -> Iterable[Asset]:
        for asset in self.assets_index.values():
            if extensions is None or asset.relative_path.suffix in extensions:
                yield asset


@dataclass
class Asset:
    asset_directory: Path
    absolute_path: Path
    relative_path: Path

    @property
    def alias(self) -> str:
        return self.relative_path.as_posix().replace(" ", "_").replace("/", ".")

    def get_output_file(self, tag: str) -> Path:
        return self._get_related_file(".output", tag)

    def _get_related_file(self, prefix: str, tag: str = "") -> Path:
        file = self.asset_directory / f"{prefix}{tag}" / self.relative_path
        file.parent.mkdir(parents=True, exist_ok=True)
        return file


GERBER_ASSET_LOADER_INSTANCE = AssetLoader2(GERBER_ASSETS_DIRECTORY)
GERBER_ASSET_LOADER_INSTANCE.detect_assets()
GERBER_ASSETS_INDEX = list(
    GERBER_ASSET_LOADER_INSTANCE.iter_assets(
        tuple(GERBER_EXTENSION_TO_FILE_TYPE_MAPPING.keys())
    )
)


@dataclass
class ConfigBase:
    """Base configuration for the test."""

    xfail: bool = False
    xfail_message: str = "Test is expected to fail"
    skip: bool = False
    skip_reason: str = "Test is skipped"


ConfigT = TypeVar("ConfigT", bound=ConfigBase)


class CaseGenerator(Generic[ConfigT]):
    """List of all configurations for all tests."""

    def __init__(
        self,
        asset_index: list[Asset],
        config_overrides: dict[str, ConfigT],
        default_config_factory: type[ConfigT],
    ) -> None:
        self.asset_index = asset_index
        self.config_overrides_unresolved = config_overrides
        self.config_overrides_resolved: dict[str, ConfigT] = {}
        self.default_config_factory = default_config_factory

        self.expand_globs_in_config_overrides()

    def expand_globs_in_config_overrides(self) -> None:
        for override_glob, config in self.config_overrides_unresolved.items():
            for asset in self.asset_index:
                if fnmatch.fnmatch(asset.alias, override_glob):
                    self.config_overrides_resolved[asset.alias] = config

    def __iter__(self) -> Generator[tuple[Asset, ConfigT], None, None]:
        def _() -> Generator[tuple[Asset, ConfigT], None, None]:
            default_config = self.default_config_factory()

            for asset in self.asset_index:
                yield (
                    asset,
                    self.config_overrides_resolved.get(asset.alias, default_config),
                )

        return _()

    @property
    def parametrize(self) -> pytest.MarkDecorator:
        return pytest.mark.parametrize(
            ("asset", "config"),
            self,
            ids=[a.alias for a in GERBER_ASSETS_INDEX],
        )


_RGBA_PIXEL: TypeAlias = Tuple[int, int, int, int]


def highlight_differences(first: Image.Image, second: Image.Image) -> Image.Image:
    """
    Highlight the differences between two images.
    """
    max_width = max(first.width, second.width)
    max_height = max(first.height, second.height)

    # Pad and center images
    img1_centered = pad_and_center(first, max_width, max_height, (0, 0, 0, 0))
    img2_centered = pad_and_center(second, max_width, max_height, (0, 0, 0, 0))

    diff_img = Image.new("RGBA", (max_width, max_height))

    draw = ImageDraw.Draw(diff_img)
    for x in range(max_width):
        for y in range(max_height):
            r1, g1, b1, a1 = cast("_RGBA_PIXEL", img1_centered.getpixel((x, y)))
            r2, g2, b2, a2 = cast("_RGBA_PIXEL", img2_centered.getpixel((x, y)))
            draw.point(
                (x, y),
                fill=(
                    abs(r1 - r2),
                    abs(g1 - g2),
                    abs(b1 - b2),
                    255 - abs(a1 - a2),
                ),
            )

    return diff_img


def pad_and_center(
    img: Image.Image,
    target_width: int,
    target_height: int,
    fill_color: tuple[int, ...] | int,
) -> Image.Image:
    """
    Pad and center the image to the target dimensions.
    """
    result = Image.new("RGBA", (target_width, target_height), fill_color)
    left = (target_width - img.width) // 2
    top = (target_height - img.height) // 2
    result.paste(img, (left, top))
    return result


T = TypeVar("T", bound=Optional[Any])


class JsonWalker:
    """Walks through a JSON-like data structure and applies callbacks to each element.

    Walking is done left-to-right in a depth-first manner.
    """

    def __init__(
        self,
        on_dict: Optional[Callable[[dict[str, Any]], None]] = None,
        on_list: Optional[Callable[[list[Any]], None]] = None,
        on_string: Optional[Callable[[str], None]] = None,
        on_number: Optional[Callable[[Union[float, int]], None]] = None,
        on_bool: Optional[Callable[[bool], None]] = None,
        on_none: Optional[Callable[[None], None]] = None,
    ) -> None:
        if on_dict is not None:
            self.on_dict = on_dict  # type: ignore[assignment]

        if on_list is not None:
            self.on_list = on_list  # type: ignore[assignment]

        if on_string is not None:
            self.on_string = on_string  # type: ignore[assignment]

        if on_number is not None:
            self.on_number = on_number  # type: ignore[assignment]

        if on_bool is not None:
            self.on_bool = on_bool  # type: ignore[assignment]

        if on_none is not None:
            self.on_none = on_none  # type: ignore[assignment]

    def walk(self, data: T) -> T:
        return self._walk_any(data)

    def _walk_any(self, data: T) -> T:
        if isinstance(data, dict):
            self.on_dict(data)
            for key, value in data.items():
                data[key] = self._walk_any(value)
            return cast("T", data)

        if isinstance(data, list):
            self.on_list(data)
            for i, value in enumerate(data):
                data[i] = self._walk_any(value)
            return cast("T", data)

        if isinstance(data, str):
            return cast("T", self.on_string(data))

        if isinstance(data, (int, float)):
            return cast("T", self.on_number(float(data)))

        if isinstance(data, bool):
            return cast("T", self.on_bool(data))

        if data is None:
            return self.on_none(data)  # type: ignore[unreachable, no-any-return, func-returns-value]

        raise TypeError(type(data))

    def on_dict(self, data: dict[str, Any]) -> dict[str, Any]:
        return data

    def on_list(self, data: list[Any]) -> list[Any]:
        return data

    def on_string(self, data: str) -> str:
        return data

    def on_number(self, data: float) -> float:
        return data

    def on_bool(self, data: bool) -> bool:  # noqa: FBT001
        return data

    def on_none(self, data: None) -> None:
        return data
