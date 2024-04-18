"""Common exception related tools."""

from __future__ import annotations

from typing import NoReturn


def throw(exception: Exception) -> NoReturn:
    """Raise given exception."""
    raise exception
