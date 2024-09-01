from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path


class Asset:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> str:
        raise NotImplementedError


class TextAsset(Asset):
    def load(self, encoding: str = "utf-8", **kwargs: Any) -> str:
        return self.path.read_text(encoding=encoding, **kwargs)


class GerberX3Assert(TextAsset):
    pass


class ExcellonAssert(Asset):
    pass
