from __future__ import annotations

from typing import Iterable

from pygerber.gerber.api._composite_view import CompositeView


class Project:
    """The `Project` class is a representation of a project composed out of multiple
    Gerber files composed into multiple views.

    It is primarily a container object for `CompositeView`.
    """

    def __init__(
        self,
        *,
        top: CompositeView,
        inner: Iterable[CompositeView],
        bottom: CompositeView,
    ) -> None:
        self._top = top
        self._inner = tuple(inner)
        self._bottom = bottom

    @property
    def top(self) -> CompositeView:
        """Get top view."""
        return self._top

    @property
    def inner(self) -> tuple[CompositeView, ...]:
        """Get inner views."""
        return self._inner

    @property
    def bottom(self) -> CompositeView:
        """Get bottom view."""
        return self._bottom

    def __str__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(top={self._top}, "
            f"inner={self._inner}, bottom={self._bottom})"
        )
