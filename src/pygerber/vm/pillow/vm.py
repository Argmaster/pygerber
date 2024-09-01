"""`pillow` module contains concrete implementation of `VirtualMachine` using Pillow
library.
"""

from __future__ import annotations

import math
import operator
from typing import Callable, Generator, Optional, Sequence

from PIL import Image, ImageDraw, ImageOps

from pygerber.vm.commands import Arc, Line, PasteLayer, Shape
from pygerber.vm.pillow.errors import DPMMTooSmallError
from pygerber.vm.rvmc import RVMC
from pygerber.vm.types.box import AutoBox, FixedBox
from pygerber.vm.types.errors import PasteDeferredLayerNotAllowedError
from pygerber.vm.types.layer_id import LayerID
from pygerber.vm.types.style import Style
from pygerber.vm.types.vector import Vector
from pygerber.vm.vm import (
    DeferredLayer,
    EagerLayer,
    Layer,
    Result,
    VirtualMachine,
)

FULL_ANGLE_DEGREES = 360

DECREASE_ANGLE = (operator.sub, operator.gt)
INCREASE_ANGLE = (operator.add, operator.lt)

MIN_SEGMENT_COUNT = 12


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


class PillowEagerLayer(EagerLayer):
    """`PillowEagerLayer` class represents drawing space of known fixed size.

    It is specifically used by `PillowVirtualMachine` class.
    """

    def __init__(self, dpmm: int, layer_id: LayerID, box: FixedBox) -> None:
        super().__init__(layer_id, box)
        self.dpmm = dpmm
        self.pixel_size = (
            self.to_pixel(self.box.width),
            self.to_pixel(self.box.height),
        )
        self.image = Image.new("1", self.pixel_size, 0)
        self.draw = ImageDraw.Draw(self.image)

    def to_pixel(self, value: float) -> int:
        """Convert value in mm to pixels."""
        return int(value * self.dpmm)


class PillowDeferredLayer(DeferredLayer):
    """`PillowDeferredLayer` class represents drawing space of size unknown at time of
    creation of layer.

    It is specifically used by `PillowVirtualMachine` class.
    """

    def __init__(self, dpmm: int, layer_id: LayerID, box: AutoBox) -> None:
        super().__init__(layer_id, box)
        self.dpmm = dpmm


class PillowVirtualMachine(VirtualMachine):
    """Execute drawing commands using Pillow library."""

    def __init__(self, dpmm: int) -> None:
        super().__init__()
        self.dpmm = dpmm
        self.angle_length_to_segment_count = lambda angle_length: (
            segment_count
            if (segment_count := angle_length * 2) > MIN_SEGMENT_COUNT
            else MIN_SEGMENT_COUNT
        )

    @property
    def layer(self) -> PillowEagerLayer:
        """Get current layer."""
        return super().layer  # type: ignore[return-value]

    def create_eager_layer(self, layer_id: LayerID, box: FixedBox) -> Layer:
        """Create new eager layer instances (factory method)."""
        return PillowEagerLayer(self.dpmm, layer_id, box)

    def create_deferred_layer(self, layer_id: LayerID, box: AutoBox) -> Layer:
        """Create new deferred layer instances (factory method)."""
        return PillowDeferredLayer(self.dpmm, layer_id, box)

    def on_shape_eager(self, command: Shape) -> None:
        """Visit shape command."""
        points: list[tuple[float, float]] = []
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
    ) -> Generator[tuple[float, float], None, None]:
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
        angle_length = (angle_delta / 360) * (command.get_radius() * 2 * math.pi)
        angle_length_pixels = self.to_pixel(angle_length)
        segment_count = self.angle_length_to_segment_count(angle_length_pixels)

        if segment_count < 1:
            raise DPMMTooSmallError(self.dpmm)

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

        yield command.start.xy

        for angle in angle_generator:
            offset_vector = Vector(
                x=radius * math.cos(math.radians(angle)),
                y=radius * math.sin(math.radians(angle)),
            )

            yield (command.center + offset_vector).xy

        yield command.end.xy

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

    def _polygon(
        self, points: Sequence[tuple[float, float]], *, negative: bool
    ) -> None:
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

    def on_paste_layer_eager(self, command: PasteLayer) -> None:
        """Visit `PasteLayer` command."""
        source_layer = self.get_layer(command.source_layer_id)

        if isinstance(source_layer, PillowDeferredLayer):
            raise PasteDeferredLayerNotAllowedError(command.source_layer_id)

        assert isinstance(source_layer, PillowEagerLayer)
        target_layer = self.layer

        source_width_half = source_layer.box.width / 2
        source_height_half = source_layer.box.height / 2

        if command.is_negative:
            image = ImageOps.invert(source_layer.image.convert("L")).convert("1")
        else:
            image = source_layer.image

        target_layer.image.paste(
            image,
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

    def to_pixel(self, value: float) -> int:
        """Convert value in mm to pixels."""
        return int(value * self.dpmm)

    def correct_center_x(self, x: float) -> float:
        """Correct x coordinate for center."""
        offset = self.layer.box.center.x - self.layer.box.width / 2
        return x - offset

    def correct_center_y(self, y: float) -> float:
        """Correct x coordinate for center."""
        offset = self.layer.box.center.y - self.layer.box.height / 2
        return y - offset

    def get_color(self, *, negative: bool) -> int:
        """Get color for positive or negative."""
        return 0 if negative else 1

    def run(self, rvmc: RVMC) -> PillowResult:
        """Execute all commands."""
        super().run(rvmc)

        layer = self._layers.get(LayerID(id="%main%"), None)

        if layer is None:
            return PillowResult(None)

        assert isinstance(layer, PillowEagerLayer)

        return PillowResult(layer.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM))
