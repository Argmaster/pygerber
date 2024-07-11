"""`pillow` module contains concrete implementation of `VirtualMachine` using Pillow
library.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.vm.base import VirtualMachine
from pygerber.vm.commands.layer import EndLayer, PasteLayer, StartLayer
from pygerber.vm.commands.polygon import Polygon

if TYPE_CHECKING:
    from PIL import Image


class PillowVirtualMachine(VirtualMachine):
    """Execute drawing commands using Pillow library."""

    def __init__(self) -> None:
        super().__init__()
        self.layer_stack: list[Image.Image] = []

    def on_polygon(self, command: Polygon) -> None:
        """Visit polygon command."""

    def on_start_layer(self, command: StartLayer) -> None:
        """Visit start layer command."""

    def on_end_layer(self, command: EndLayer) -> None:
        """Visit start end command."""

    def on_paste_layer(self, command: PasteLayer) -> None:
        """Visit paste layer command."""
