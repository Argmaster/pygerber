"""`pygerber.nodes.math.expression` module contains definition of `Expression`
class.
"""

from __future__ import annotations

from pygerber.gerber.ast.nodes.base import Node


class Expression(Node):
    """Represents math expression expression."""
