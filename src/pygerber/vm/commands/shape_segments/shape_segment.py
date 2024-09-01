"""`base` module contains ShapeSegment class used as base class for all Shape
segments.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pyparsing as pp
from pydantic import BaseModel

from pygerber.vm.types import AutoBox, Matrix3x3

if TYPE_CHECKING:
    from typing_extensions import Self


class ShapeSegment(BaseModel):
    """Base class for shape segment types."""

    @pp.cached_property
    def outer_box(self) -> AutoBox:
        """Get outer box of shape segment."""
        raise NotImplementedError

    def transform(self, transform: Matrix3x3) -> Self:
        """Transform line."""
        raise NotImplementedError
