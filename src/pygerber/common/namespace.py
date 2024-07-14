"""`namespace` module contains definition of `Namespace` class used to prevent
instantiation of derived classes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing import NoReturn


class NamespaceMeta(type):
    """Metaclass that prevents instantiation of the class."""

    def __call__(cls, *_: Any, **__: Any) -> NoReturn:
        """Raise a TypeError when trying to instantiate the class."""
        msg = "Cannot instantiate class"
        raise TypeError(msg)


class Namespace(metaclass=NamespaceMeta):
    """Base class that prevents instantiation of derived classes."""
