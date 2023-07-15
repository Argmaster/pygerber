"""Tools related to typing."""
from __future__ import annotations

from typing import Any


def assert_isinstance(__obj: Any, __class_or_tuple: type | tuple[type]) -> None:
    """Shortcut for checking if object is an instance of expected class."""
    if not isinstance(__obj, __class_or_tuple):
        msg = f"Expected {__obj} to be instance of {__class_or_tuple}."
        raise TypeError(msg)
