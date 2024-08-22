"""`pygerber.nodes.aperture.ADC` module contains definition of `AD` class."""

from __future__ import annotations

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.types import ApertureIdStr


class AD(Node):
    """Common base class for all commands adding new apertures."""

    aperture_id: ApertureIdStr
