"""`shape_segments` module contains classes representing shape segments."""

from __future__ import annotations

from pygerber.vm.commands.shape_segments.arc import Arc
from pygerber.vm.commands.shape_segments.line import Line
from pygerber.vm.commands.shape_segments.shape_segment import ShapeSegment

__all__ = ["ShapeSegment", "Line", "Arc"]
