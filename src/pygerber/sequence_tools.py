"""Convenience tools for operating on sequences."""

from __future__ import annotations

from typing import Iterable, TypeVar

from pyparsing import ParseResults

T = TypeVar("T")


def flatten_list(sequence: list[T]) -> list[T]:
    """Flatten a sequence."""
    out = []

    for item in sequence:
        if isinstance(item, list):
            out.extend(flatten_list(item))
        else:
            out.append(item)

    return out


def flatten(sequence: Iterable[T]) -> Iterable[T]:
    """Flatten a sequence."""
    for item in sequence:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item


def unwrap(item: T) -> T:
    """Unwrap item wrapped in sequences."""
    try:
        while isinstance(item, (list, tuple, ParseResults)):
            item = item[0]  # type: ignore[pylance]
    except (TypeError, IndexError):
        pass

    return item
