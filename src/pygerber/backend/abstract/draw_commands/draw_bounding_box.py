"""BoundingBox component for creating apertures."""

from __future__ import annotations

from functools import cached_property

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.state_enums import Polarity


class DrawBoundingBox(DrawCommand):
    """Description of BoundingBox component."""

    bounding_box: BoundingBox
    outline_padding: Offset

    def __init__(
        self,
        backend: Backend,
        polarity: Polarity,
        bounding_box: BoundingBox,
        outline_padding: Offset,
    ) -> None:
        """Initialize draw command."""
        super().__init__(backend, polarity)
        self.bounding_box = bounding_box
        self.outline_padding = outline_padding

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        return self._bounding_box

    @cached_property
    def _bounding_box(self) -> BoundingBox:
        return self.bounding_box + self.outline_padding
