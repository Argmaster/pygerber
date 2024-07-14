"""`pillow` module contains concrete implementation of `VirtualMachine` using Pillow
library.
"""

from __future__ import annotations

import math
import operator
from typing import Callable, Generator, Optional, Sequence

from PIL import Image, ImageDraw

from pygerber.vm.base import Result, VirtualMachine
from pygerber.vm.commands.command import Command
from pygerber.vm.commands.layer import EndLayer, PasteLayer, StartLayer
from pygerber.vm.commands.shape import Arc, Line, Shape
from pygerber.vm.pillow.errors import (
    LayerNotFoundError,
    NoLayerSetError,
)
from pygerber.vm.types.box import Box
from pygerber.vm.types.layer_id import LayerID
from pygerber.vm.types.style import Style
from pygerber.vm.types.unit import Unit
from pygerber.vm.types.vector import Vector

FULL_ANGLE_DEGREES = 360

DECREASE_ANGLE = (operator.sub, operator.gt)
INCREASE_ANGLE = (operator.add, operator.lt)


class PillowResult(Result):
    """Result of drawing commands."""

    def __init__(self, image: Optional[Image.Image]) -> None:
        self.image = image

    def is_success(self) -> bool:
        """Check if result is successful."""
        return self.image is not None

    def get_image(self, style: Style = Style.presets.COPPER) -> Image.Image:
        """Get image with given color scheme."""
        assert isinstance(style, Style)
        if self.image is None:
            msg = "Image is not available."
            raise ValueError(msg)
        return self.image


class _PillowLayer:
    """Layer in PillowVirtualMachine."""

    def __init__(self, dpmm: int, box: Box) -> None:
        self.dpmm = dpmm
        self.box = box
        self.pixel_size = (
            self.to_pixel(self.box.width),
            self.to_pixel(self.box.height),
        )
        self.image = Image.new("1", self.pixel_size, 0)
        self.draw = ImageDraw.Draw(self.image)

    def to_pixel(self, value: float | Unit) -> int:
        """Convert value in mm to pixels."""
        if isinstance(value, Unit):
            return int(value.value * self.dpmm)
        return int(value * self.dpmm)


class PillowVirtualMachine(VirtualMachine):
    """Execute drawing commands using Pillow library."""

    def __init__(self, dpmm: int) -> None:
        super().__init__()
        self.dpmm = dpmm
        self.angle_length_to_segment_count_ratio = 0.314
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

    def on_shape(self, command: Shape) -> None:
        """Visit shape command."""
        points: list[tuple[Unit, Unit]] = []
        for segment in command.commands:
            if isinstance(segment, Line):
                start = (segment.start.x, segment.start.y)
                if len(points) == 0 or points[-1] != start:
                    points.append(
                        (segment.start.x, segment.start.y),
                    )
                points.append(
                    (segment.end.x, segment.end.y),
                )
            elif isinstance(segment, Arc):
                start = (segment.start.x, segment.start.y)
                if len(points) == 0 or points[-1] != start:
                    points.append(
                        (segment.start.x, segment.start.y),
                    )
                points.extend(self._calculate_arc_points(segment))
                points.append(
                    (segment.end.x, segment.end.y),
                )
            else:
                raise NotImplementedError

        self._polygon(points, negative=command.negative)

    def _calculate_arc_points(
        self, command: Arc
    ) -> Generator[tuple[Unit, Unit], None, None]:
        """Calculate points on arc."""
        start_angle = (
            command.get_relative_start_point().angle_between(
                Vector.unit.x,
            )
            % 360
        )
        end_angle = (
            command.get_relative_end_point().angle_between(
                Vector.unit.x,
            )
            % 360
        )
        assert start_angle >= 0
        assert end_angle >= 0

        assert start_angle < FULL_ANGLE_DEGREES
        assert end_angle < FULL_ANGLE_DEGREES

        angle_delta = abs(start_angle - end_angle)
        angle_length = (angle_delta / 360) * (command.get_radius().value * 2 * math.pi)
        angle_length_pixels = self.to_pixel(angle_length)
        segment_count = angle_length_pixels * self.angle_length_to_segment_count_ratio
        angle_delta = angle_delta / segment_count

        assert angle_delta > 0

        angle_generator: Generator[float, None, None]

        if start_angle <= end_angle:
            if command.clockwise:
                end_angle -= FULL_ANGLE_DEGREES
                angle_generator = self._generate_arc_angles(
                    start_angle, end_angle, angle_delta, *DECREASE_ANGLE
                )
            else:
                angle_generator = self._generate_arc_angles(
                    start_angle, end_angle, angle_delta, *INCREASE_ANGLE
                )
        elif command.clockwise:
            angle_generator = self._generate_arc_angles(
                start_angle, end_angle, angle_delta, *DECREASE_ANGLE
            )
        else:
            end_angle += FULL_ANGLE_DEGREES
            angle_generator = self._generate_arc_angles(
                start_angle, end_angle, angle_delta, *INCREASE_ANGLE
            )

        radius = command.get_radius()

        for angle in angle_generator:
            offset_vector = Vector(
                x=radius * math.cos(math.radians(angle)),
                y=radius * math.sin(math.radians(angle)),
            )

            yield (command.center + offset_vector).xy

    def _generate_arc_angles(
        self,
        start: float,
        end: float,
        delta: float,
        apply_delta: Callable[[float, float], float],
        compare_angles: Callable[[float, float], bool],
    ) -> Generator[float, None, None]:
        current_angle = start
        while compare_angles(current_angle, end):
            yield current_angle
            current_angle = apply_delta(current_angle, delta)
        yield end

    def _polygon(self, points: Sequence[tuple[Unit, Unit]], *, negative: bool) -> None:
        """Draw a polygon."""
        self.layer.draw.polygon(
            [
                (
                    self.to_pixel(self.correct_center_x(x)),
                    self.to_pixel(self.correct_center_y(y)),
                )
                for (x, y) in points
            ],
            fill=self.get_color(negative=negative),
            width=0,
        )

    def on_start_layer(self, command: StartLayer) -> None:
        """Visit start layer command."""
        layer = _PillowLayer(self.dpmm, command.box)
        self.layers[command.id] = layer
        self.layer_stack.append(layer)

    def on_end_layer(self, command: EndLayer) -> None:
        """Visit start end command."""
        assert len(self.layer_stack) > 0
        assert isinstance(command, EndLayer)
        self.layer_stack.pop()

    def on_paste_layer(self, command: PasteLayer) -> None:
        """Visit paste layer command."""
        source_layer = self.layers.get(command.id, None)
        if source_layer is None:
            raise LayerNotFoundError(command.id)

        target_layer = self.layers.get(command.target_id, None)
        if target_layer is None:
            raise LayerNotFoundError(command.target_id)

        source_width_half = source_layer.box.width / 2
        source_height_half = source_layer.box.height / 2

        target_layer.image.paste(
            source_layer.image,
            (
                self.to_pixel(
                    self.correct_center_x(command.center.x - source_width_half)
                ),
                self.to_pixel(
                    self.correct_center_y(command.center.y - source_height_half)
                ),
            ),
            mask=source_layer.image,
        )

    def to_pixel(self, value: float | Unit) -> int:
        """Convert value in mm to pixels."""
        if isinstance(value, Unit):
            return int(value.value * self.dpmm)
        return int(value * self.dpmm)

    def correct_center_x(self, x: float | Unit) -> float:
        """Correct x coordinate for center."""
        offset = self.layer.box.center.x.value - self.layer.box.width / 2
        if isinstance(x, Unit):
            return x.value - offset
        return x - offset

    def correct_center_y(self, y: float | Unit) -> float:
        """Correct x coordinate for center."""
        offset = self.layer.box.center.y.value - self.layer.box.height / 2
        if isinstance(y, Unit):
            return y.value - offset
        return y - offset

    def get_color(self, *, negative: bool) -> int:
        """Get color for positive or negative."""
        return 0 if negative else 1

    def run(self, commands: Sequence[Command]) -> PillowResult:
        """Execute all commands."""
        super().run(commands)

        layer = self.layers.get(LayerID(id="main"), None)

        self.reset()

        if layer is None:
            return PillowResult(None)
        return PillowResult(layer.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM))
