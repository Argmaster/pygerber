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
        internal_layers: Iterable[CompositeView],
        bottom: CompositeView,
    ) -> None:
        self.top = top
        self.internal_layers = tuple(internal_layers)
        self.bottom = bottom
