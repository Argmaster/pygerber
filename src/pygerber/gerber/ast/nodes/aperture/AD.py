"""`pygerber.nodes.aperture.ADC` module contains definition of `AD` class."""

from __future__ import annotations

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.types import ApertureIdStr


class AD(Node):
    """Common base class for all commands adding new apertures."""

    aperture_id: ApertureIdStr
