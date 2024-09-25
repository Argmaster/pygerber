"""`base` module contains ShapeSegment class used as base class for all Shape
segments.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pyparsing as pp

from pygerber.gerber.ast.nodes.model import ModelType
from pygerber.vm.types import Box, Matrix3x3

if TYPE_CHECKING:
    from typing_extensions import Self


class ShapeSegment(ModelType):
    """Base class for shape segment types."""

    @pp.cached_property
    def outer_box(self) -> Box:
        """Get outer box of shape segment."""
        raise NotImplementedError

    def transform(self, transform: Matrix3x3) -> Self:
        """Transform line."""
        raise NotImplementedError
