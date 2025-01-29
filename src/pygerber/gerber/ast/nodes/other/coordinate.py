"""`pygerber.nodes.other.Coordinate` module contains definition of `Coordinate`
class.
"""

from __future__ import annotations

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.types import PackedCoordinateStr


class Coordinate(Node):
    """Represents Coordinate node."""

    value: PackedCoordinateStr
