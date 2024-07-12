"""`pillow` module contains concrete implementation of `VirtualMachine` using Pillow
library.
"""

from __future__ import annotations

from typing import Optional, Sequence

from PIL import Image, ImageDraw

from pygerber.vm.base import Result, VirtualMachine
from pygerber.vm.commands.command import Command
from pygerber.vm.commands.layer import EndLayer, PasteLayer, StartLayer
from pygerber.vm.commands.polygon import Arc, Line, Polygon
from pygerber.vm.pillow.errors import NoLayerSetError
from pygerber.vm.types.layer_id import LayerID
from pygerber.vm.types.style import Style
from pygerber.vm.types.unit import Unit


class PillowResult(Result):
    """Result of drawing commands."""

    def __init__(self, image: Optional[Image.Image]) -> None:
        self.image = image

    def is_success(self) -> bool:
        """Check if result is successful."""
        return self.image is not None

    def get_image(self, style: Style) -> Image.Image:  # noqa: ARG002
        """Get image with given color scheme."""
        if self.image is None:
            msg = "Image is not available."
            raise ValueError(msg)
        return self.image


class _PillowLayer:
    """Layer in PillowVirtualMachine."""

    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
        self.image = Image.new("1", size, 0)
        self.draw = ImageDraw.Draw(self.image)


class PillowVirtualMachine(VirtualMachine):
    """Execute drawing commands using Pillow library."""

    def __init__(self, dpmm: int) -> None:
        super().__init__()
        self.dpmm = dpmm
        self.reset()

    def reset(self) -> None:
        """Reset state of the virtual machine."""
        self.layers: dict[LayerID, _PillowLayer] = {}
        self.layer_stack: list[_PillowLayer] = []

    @property
    def layer(self) -> _PillowLayer:
        """Get current layer."""
        if self.layer_stack:
            return self.layer_stack[-1]

        raise NoLayerSetError

    def on_polygon(self, command: Polygon) -> None:
        """Visit polygon command."""
        points: list[tuple[int, int]] = []
        for segment in command.commands:
            if isinstance(segment, Line):
                points.append(
                    (
                        self.to_pixel(segment.start.x),
                        self.to_pixel(segment.start.y),
                    ),
                )
            elif isinstance(segment, Arc):
                # Needs implementation of arc calculation logic.
                points.append(
                    (
                        self.to_pixel(segment.start.x),
                        self.to_pixel(segment.start.y),
                    ),
                )
            else:
                raise NotImplementedError

        self.layer.draw.polygon(points, fill=self.get_color(negative=command.negative))

    def on_start_layer(self, command: StartLayer) -> None:
        """Visit start layer command."""
        layer = _PillowLayer(
            (
                self.to_pixel(command.box.width),
                self.to_pixel(command.box.height),
            ),
        )
        self.layers[command.id] = layer
        self.layer_stack.append(layer)

    def on_end_layer(self, command: EndLayer) -> None:
        """Visit start end command."""

    def on_paste_layer(self, command: PasteLayer) -> None:
        """Visit paste layer command."""

    def to_pixel(self, value: float | Unit) -> int:
        """Convert value in mm to pixels."""
        if isinstance(value, Unit):
            return int(value.value * self.dpmm)
        return int(value * self.dpmm)

    def get_color(self, *, negative: bool) -> int:
        """Get color for positive or negative."""
        return 0 if negative else 1

    def run(self, commands: Sequence[Command]) -> Result:
        """Execute all commands."""
        super().run(commands)

        layer = self.layers.get(LayerID(id="main"), None)

        self.reset()

        if layer is None:
            return PillowResult(None)
        return PillowResult(layer.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM))
