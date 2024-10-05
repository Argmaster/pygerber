"""The `vm` module contains concrete implementation of `VirtualMachine` using
Shapely library.
"""

from __future__ import annotations

import importlib
import importlib.util
import math
import operator
from contextlib import suppress
from pathlib import Path
from typing import Callable, Generator, Optional, Sequence, TextIO

import numpy as np

from pygerber.vm.commands import Arc, Line, Shape
from pygerber.vm.commands.paste import PasteLayer
from pygerber.vm.rvmc import RVMC
from pygerber.vm.shapely.errors import ShapelyNotInstalledError
from pygerber.vm.types import Box, LayerID, NoMainLayerError, Style, Vector
from pygerber.vm.types.errors import PasteDeferredLayerNotAllowedError
from pygerber.vm.vm import DeferredLayer, EagerLayer, Layer, Result, VirtualMachine

FULL_ANGLE_DEGREES = 360

DECREASE_ANGLE = (operator.sub, operator.gt)
INCREASE_ANGLE = (operator.add, operator.lt)

_IS_shapely_AVAILABLE: Optional[bool] = None


def is_shapely_available() -> bool:
    """Check if the language server feature is available."""
    global _IS_shapely_AVAILABLE  # noqa: PLW0603

    if _IS_shapely_AVAILABLE is None:
        try:
            _spec_shapely = importlib.util.find_spec("shapely")

        except (ImportError, ValueError):
            _IS_shapely_AVAILABLE = False

        else:
            _IS_shapely_AVAILABLE = _spec_shapely is not None

    return _IS_shapely_AVAILABLE


with suppress(Exception):
    import shapely as sh
    import shapely.strtree as shtree


class ShapelyResult(Result):
    """The `ShapelyResult` class is a wrapper around items returned
    `ShapelyVirtualMachine` class as a result of executing rendering instruction.
    """

    def __init__(self, main_box: Box, shape: sh.geometry.base.BaseGeometry) -> None:
        super().__init__(main_box)
        if not is_shapely_available():
            raise ShapelyNotInstalledError

        self.shape = shape

    def save_svg(
        self,
        destination: str | Path | TextIO,
        color: Style = Style.presets.COPPER_ALPHA,
    ) -> None:
        """Save result to a file or buffer in SVG format.

        Parameters
        ----------
        destination : str | Path | TextIO
            `str` and `Path` objects are interpreted as file paths and opened with
            truncation. `TextIO`-like (files, StringIO) objects are written to directly.
        color : Style, optional
            Color to use for SVG, background is ignored as it is always rendered as
            empty space, so only foreground applies, by default
            Style.presets.COPPER_ALPHA

        """
        if isinstance(destination, (str, Path)):
            with Path(destination).open("w") as file:
                self._dump_svg(file, color)

        elif isinstance(destination, TextIO):
            self._dump_svg(destination, color)

        else:
            raise NotImplementedError(type(destination))

    def _dump_svg(self, out: TextIO, color: Style) -> None:
        out.write(
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
        )
        if self.shape.is_empty:
            out.write("/>")
            return

        xmin, ymin, xmax, ymax = self.shape.bounds

        dx = xmax - xmin
        dy = ymax - ymin
        width = dx
        height = dy

        fill_color = color.foreground.to_hex()

        view_box = f"{xmin} {ymin} {dx} {dy}"
        transform = f"matrix(1,0,0,-1,0,{ymax + ymin})"

        out.write(f'width="{width}" ')
        out.write(f'height="{height}" ')
        out.write(f'viewBox="{view_box}" ')
        out.write('preserveAspectRatio="xMidYMid meet" ')
        out.write(">")
        out.write(
            (
                f'<g transform="{transform}">'
                f"{self.shape.svg(scale_factor=0.0, fill_color=fill_color)}"
                "</g>"
            ).replace('stroke="#555555"', 'stroke="#00000000"')
        )
        out.write("</svg>")


class ShapelyEagerLayer(EagerLayer):
    """`ShapelyEagerLayer` class represents drawing space of known fixed size.

    It is specifically used by `ShapelyEagerLayer` class.
    """

    def __init__(self, layer_id: LayerID, origin: Vector, box: Box) -> None:
        super().__init__(layer_id, box, origin)
        if not is_shapely_available():
            raise ShapelyNotInstalledError

        self.shape: list[sh.Polygon] = []


class ShapelyDeferredLayer(DeferredLayer):
    """`ShapelyDeferredLayer` class represents drawing space of size unknown at time of
    creation of layer.

    It is specifically used by `ShapelyDeferredLayer` class.
    """


class ShapelyVirtualMachine(VirtualMachine):
    """The `ShapelyVirtualMachine` class is a concrete implementation of
    `VirtualMachine` which uses Shapely library for rendering commands.
    """

    def __init__(
        self,
        angle_length_to_segment_count: Callable[[float], int] = lambda angle_length: (
            int(abs(angle_length) * 0.4 + 24)
        ),
        grid_size: Optional[float] = None,
    ) -> None:
        super().__init__()
        if not is_shapely_available():
            raise ShapelyNotInstalledError

        self.angle_length_to_segment_count = angle_length_to_segment_count
        self.grid_size = grid_size

    @property
    def layer(self) -> ShapelyEagerLayer:
        """Get current layer."""
        return super().layer  # type: ignore[return-value]

    def create_eager_layer(self, layer_id: LayerID, box: Box, origin: Vector) -> Layer:
        """Create new eager layer instances (factory method)."""
        return ShapelyEagerLayer(layer_id, origin, box)

    def create_deferred_layer(self, layer_id: LayerID, origin: Vector) -> Layer:
        """Create new deferred layer instances (factory method)."""
        return ShapelyDeferredLayer(layer_id, origin, commands=[])

    def on_shape_eager(self, command: Shape) -> None:
        """Visit shape command."""
        points: list[tuple[float, float]] = []

        for segment in command.commands:
            if isinstance(segment, Line):
                start = (segment.start.x, segment.start.y)
                if len(points) == 0 or points[-1] != start:
                    points.append(start)

                end = (segment.end.x, segment.end.y)
                points.append(end)

            elif isinstance(segment, Arc):
                start = (segment.start.x, segment.start.y)
                if len(points) == 0 or points[-1] != start:
                    points.append(start)

                points.extend(self._calculate_arc_points(segment))

                end = (segment.end.x, segment.end.y)
                if end != points[-1]:
                    points.append(end)
            else:
                raise NotImplementedError(type(segment))

        if points:
            points.append(points[0])

        self._add_polygon(points, is_negative=command.is_negative)

    def _add_polygon(
        self, points: Sequence[tuple[float, float]], *, is_negative: bool
    ) -> None:
        """Draw a polygon."""
        polygon = sh.Polygon(points)

        layer = self.layer
        x_offset = -layer.origin.x
        y_offset = -layer.origin.y

        transformed_shape = sh.transform(
            polygon,
            lambda p: np.array(
                [
                    p[:, 0] + x_offset,
                    p[:, 1] + y_offset,
                ]
            ).T,
        ).buffer(0)

        if is_negative:
            tree = shtree.STRtree(self.layer.shape)
            idx = tree.query(transformed_shape)

            for i in idx.reshape(-1):
                self.layer.shape[i] = self.layer.shape[i].difference(transformed_shape)
        else:
            self.layer.shape.append(transformed_shape)

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
        segment_count = self.angle_length_to_segment_count(angle_length)

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

    def on_paste_layer_eager(self, command: PasteLayer) -> None:
        """Visit `PasteLayer` command."""
        source_layer = self.get_layer(command.source_layer_id)

        if isinstance(source_layer, ShapelyDeferredLayer):
            raise PasteDeferredLayerNotAllowedError(command.source_layer_id)

        assert isinstance(source_layer, ShapelyEagerLayer), type(source_layer)

        layer = self.layer
        x_offset = -layer.origin.x + command.center.x
        y_offset = -layer.origin.y + command.center.y

        transformed_shape = [
            sh.transform(
                geom,
                lambda p: np.array(
                    [
                        p[:, 0] + x_offset,
                        p[:, 1] + y_offset,
                    ]
                ).T,
            )
            for geom in source_layer.shape
        ]

        if command.is_negative:
            dest_layer_tree = shtree.STRtree(self.layer.shape)
            dest_idx = dest_layer_tree.query(transformed_shape).T

            for i, j in dest_idx:
                self.layer.shape[j] = self.layer.shape[j].difference(
                    transformed_shape[i]
                )
        else:
            self.layer.shape.extend(transformed_shape)

    def run(self, rvmc: RVMC) -> ShapelyResult:
        """Execute all commands."""
        super().run(rvmc)

        layer = self._layers.get(self.MAIN_LAYER_ID, None)

        if layer is None:
            raise NoMainLayerError

        assert isinstance(layer, ShapelyEagerLayer)
        return ShapelyResult(layer.box, sh.unary_union(layer.shape))
