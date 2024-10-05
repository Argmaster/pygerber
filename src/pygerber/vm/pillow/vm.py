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
from pygerber.vm.types import (
    Box,
    LayerID,
    NoMainLayerError,
    PasteDeferredLayerNotAllowedError,
    Style,
    Vector,
)
from pygerber.vm.vm import (
    DeferredLayer,
    DrawCmdT,
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
    """The `PillowResult` class is a wrapper around items returned
    `PillowVirtualMachine` class as a result of executing rendering instruction.
    """

    def __init__(self, main_box: Box, image: Optional[Image.Image]) -> None:
        super().__init__(main_box)
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

        image = replace_color(
            self.image, (255, 255, 255, 255), style.foreground.as_rgba_int()
        )
        return replace_color_in_place(
            image, (0, 0, 0, 255), style.background.as_rgba_int()
        )

    def get_image_no_style(self) -> Image.Image:
        """Get image without any color scheme."""
        if self.image is None:
            msg = "Image is not available."
            raise ValueError(msg)

        return self.image


def replace_color(
    input_image: Image.Image,
    original: tuple[int, ...] | int,
    replacement: tuple[int, ...] | int,
    *,
    output_image_mode: str = "RGBA",
) -> Image.Image:
    """Replace `original` color from input image with `replacement` color."""
    if input_image.mode != output_image_mode:
        output_image = input_image.convert(output_image_mode)
    else:
        output_image = input_image.copy()

    replace_color_in_place(output_image, original, replacement)

    return output_image


def replace_color_in_place(
    image: Image.Image,
    original: tuple[int, ...] | int,
    replacement: tuple[int, ...] | int,
) -> Image.Image:
    """Replace `original` color from input image with `replacement` color."""
    for x in range(image.width):
        for y in range(image.height):
            if image.getpixel((x, y)) == original:
                image.putpixel((x, y), replacement)

    return image


class PillowEagerLayer(EagerLayer):
    """`PillowEagerLayer` class represents drawing space of known fixed size.

    It is specifically used by `PillowVirtualMachine` class.
    """

    def __init__(self, dpmm: int, layer_id: LayerID, box: Box, origin: Vector) -> None:
        super().__init__(layer_id, box, origin)
        self.origin = origin
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

    def __init__(
        self, dpmm: int, layer_id: LayerID, origin: Vector, commands: list[DrawCmdT]
    ) -> None:
        super().__init__(layer_id, origin, commands)
        self.dpmm = dpmm


class PillowVirtualMachine(VirtualMachine):
    """The `PillowVirtualMachine` class is a concrete implementation of
    `VirtualMachine` which uses Shapely library for rendering commands.
    """

    def __init__(self, dpmm: int) -> None:
        super().__init__()
        self.dpmm = dpmm
        self.angle_length_to_segment_count = lambda angle_length: (
            int(segment_count)
            if (segment_count := angle_length * 2) > MIN_SEGMENT_COUNT
            else MIN_SEGMENT_COUNT
        )

    @property
    def layer(self) -> PillowEagerLayer:
        """Get current layer."""
        return super().layer  # type: ignore[return-value]

    def create_eager_layer(self, layer_id: LayerID, box: Box, origin: Vector) -> Layer:
        """Create new eager layer instances (factory method)."""
        assert box.width > 0
        assert box.height > 0
        return PillowEagerLayer(self.dpmm, layer_id, box, origin)

    def create_deferred_layer(self, layer_id: LayerID, origin: Vector) -> Layer:
        """Create new deferred layer instances (factory method)."""
        return PillowDeferredLayer(self.dpmm, layer_id, origin, commands=[])

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

        self._polygon(points, is_negative=command.is_negative)

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
        self, points: Sequence[tuple[float, float]], *, is_negative: bool
    ) -> None:
        """Draw a polygon."""
        layer = self.layer
        layer_box = layer.box
        x_offset = layer_box.center.x - layer_box.width / 2
        y_offset = layer_box.center.y - layer_box.height / 2

        layer.draw.polygon(
            [
                (
                    self.to_pixel(x - x_offset),
                    self.to_pixel(y - y_offset),
                )
                for (x, y) in points
            ],
            fill=self.get_color(is_negative=is_negative),
            width=0,
        )

    def on_paste_layer_eager(self, command: PasteLayer) -> None:
        """Visit `PasteLayer` command."""
        source_layer = self.get_layer(command.source_layer_id)

        if isinstance(source_layer, PillowDeferredLayer):
            raise PasteDeferredLayerNotAllowedError(command.source_layer_id)

        assert isinstance(source_layer, PillowEagerLayer)

        if command.is_negative:
            image = ImageOps.invert(source_layer.image.convert("L")).convert("1")
        else:
            image = source_layer.image

        layer = self.layer
        layer_box = layer.box
        x_offset = layer_box.center.x - layer_box.width / 2
        y_offset = layer_box.center.y - layer_box.height / 2

        layer.image.paste(
            image,
            (
                self.to_pixel(
                    command.center.x
                    - (source_layer.box.width / 2)
                    + source_layer.box.center.x
                    - source_layer.origin.x
                    - x_offset
                ),
                self.to_pixel(
                    command.center.y
                    - (source_layer.box.height / 2)
                    + source_layer.box.center.y
                    - source_layer.origin.y
                    - y_offset
                ),
            ),
            mask=source_layer.image,
        )

    def to_pixel(self, value: float) -> int:
        """Convert value in mm to pixels."""
        return int(value * self.dpmm)

    def get_color(self, *, is_negative: bool) -> int:
        """Get color for positive or negative."""
        return 0 if is_negative else 1

    def run(self, rvmc: RVMC) -> PillowResult:
        """Execute all commands."""
        super().run(rvmc)

        layer = self._layers.get(self.MAIN_LAYER_ID, None)

        if layer is None:
            raise NoMainLayerError

        assert isinstance(layer, PillowEagerLayer)
        return PillowResult(
            layer.box, layer.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        )
