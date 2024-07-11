"""`point` module contains `Point` class used to represent 2D coordinates."""

from __future__ import annotations

from pygerber.vm.types.model import VMModelType


class Point(VMModelType):
    """Represents a point in 2D space."""

    x: float
    y: float
