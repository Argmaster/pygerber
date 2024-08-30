"""`base` module contains ShapeSegment class used as base class for all Shape
segments.
"""

from __future__ import annotations

import pyparsing as pp
from pydantic import BaseModel

from pygerber.vm.types.box import AutoBox


class ShapeSegment(BaseModel):
    """Base class for shape segment types."""

    @pp.cached_property
    def outer_box(self) -> AutoBox:
        """Get outer box of shape segment."""
        raise NotImplementedError
