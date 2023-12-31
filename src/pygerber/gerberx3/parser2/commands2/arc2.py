"""Parser level abstraction of draw arc operation for Gerber AST parser, version 2."""
from __future__ import annotations

from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.commands2.command2 import Command2


class Arc2(Command2):
    """Parser level abstraction of draw arc operation for Gerber AST parser,
    version 2.
    """

    start_point: Vector2D
    end_point: Vector2D
    center_point: Vector2D

    def get_relative_start_point(self) -> Vector2D:
        """Get starting point relative to arc center."""
        return self.start_point - self.center_point

    def get_relative_end_point(self) -> Vector2D:
        """Get ending point relative to arc center."""
        return self.end_point - self.center_point

    def get_relative_center_point(self) -> Vector2D:
        """Get center point relative to arc center."""
        return self.center_point - self.center_point

    def get_radius(self) -> Offset:
        """Get radius of circle arc."""
        return self.get_relative_start_point().length()

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of arc."""
        return BoundingBox.from_diameter(self.get_radius() * 2) + self.center_point


class CCArc2(Arc2):
    """Parser level abstraction of draw counterclockwise arc operation for Gerber AST
    parser, version 2.
    """
