"""Module contains implementation of Gerber rendering backend outputting SVG files."""
from __future__ import annotations

import importlib.util
from dataclasses import dataclass, field
from decimal import Decimal
from typing import BinaryIO, Optional

from pygerber.backend.rasterized_2d.color_scheme import ColorScheme
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.apertures2.circle2 import Circle2, NoCircle2
from pygerber.gerberx3.parser2.apertures2.macro2 import Macro2
from pygerber.gerberx3.parser2.apertures2.obround2 import Obround2
from pygerber.gerberx3.parser2.apertures2.polygon2 import Polygon2
from pygerber.gerberx3.parser2.apertures2.rectangle2 import Rectangle2
from pygerber.gerberx3.parser2.command_buffer2 import ReadonlyCommandBuffer2
from pygerber.gerberx3.parser2.commands2.arc2 import Arc2, CCArc2
from pygerber.gerberx3.parser2.commands2.buffer_command2 import BufferCommand2
from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
from pygerber.gerberx3.parser2.commands2.line2 import Line2
from pygerber.gerberx3.parser2.commands2.region2 import Region2
from pygerber.gerberx3.renderer2.abstract import (
    FormatOptions,
    ImageRef,
    Renderer2,
    Renderer2HooksABC,
)
from pygerber.gerberx3.renderer2.errors2 import DRAWSVGNotAvailableError
from pygerber.gerberx3.state_enums import Polarity

IS_SVG_BACKEND_AVAILABLE: bool = False

try:
    _spec_drawsvg = importlib.util.find_spec("drawsvg")

    IS_SVG_BACKEND_AVAILABLE = _spec_drawsvg is not None
except (ImportError, ValueError):
    IS_SVG_BACKEND_AVAILABLE = False


if IS_SVG_BACKEND_AVAILABLE:
    import drawsvg


class SvgRenderer2(Renderer2):
    """Rendering backend class for rendering SVG images."""

    def __init__(
        self,
        hooks: Optional[SvgRenderer2Hooks] = None,
    ) -> None:
        hooks = SvgRenderer2Hooks() if hooks is None else hooks
        super().__init__(hooks)


if IS_SVG_BACKEND_AVAILABLE:
    import drawsvg

    @dataclass
    class SvgRenderingFrame:
        """Rendering variable container."""

        command_buffer: ReadonlyCommandBuffer2
        bounding_box: BoundingBox
        normalize_origin_to_0_0: bool
        mask: drawsvg.Mask = field(default_factory=drawsvg.Mask)
        layer: drawsvg.Group = field(default_factory=drawsvg.Group)
        polarity: Optional[Polarity] = None
        is_region: bool = False
        flip_y: bool = True


class SvgRenderer2Hooks(Renderer2HooksABC):
    """Rendering backend hooks used to render SVG images."""

    renderer: SvgRenderer2

    def __init__(
        self,
        color_scheme: ColorScheme = ColorScheme.DEBUG_1,
        scale: Decimal = Decimal("1"),
        *,
        flip_y: bool = True,
    ) -> None:
        if not IS_SVG_BACKEND_AVAILABLE:
            raise DRAWSVGNotAvailableError
        self.color_scheme = color_scheme
        self.scale = scale
        self.flip_y = flip_y

    def init(
        self,
        renderer: Renderer2,
        command_buffer: ReadonlyCommandBuffer2,
    ) -> None:
        """Initialize rendering hooks."""
        if not isinstance(renderer, SvgRenderer2):
            raise NotImplementedError

        self.renderer = renderer
        self.command_buffer = command_buffer
        self.rendering_stack: list[SvgRenderingFrame] = [
            SvgRenderingFrame(
                command_buffer=self.command_buffer,
                bounding_box=self.command_buffer.get_bounding_box(),
                normalize_origin_to_0_0=True,
                flip_y=self.flip_y,
            ),
        ]
        self.apertures: dict[str, drawsvg.Group] = {}

    def push_render_frame(
        self,
        cmd: ReadonlyCommandBuffer2,
        *,
        normalize_origin_to_0_0: bool,
        flip_y: bool,
    ) -> None:
        """Push new segment render frame."""
        self.rendering_stack.append(
            SvgRenderingFrame(
                command_buffer=cmd,
                bounding_box=cmd.get_bounding_box(),
                normalize_origin_to_0_0=normalize_origin_to_0_0,
                flip_y=flip_y,
            ),
        )

    def pop_render_frame(self) -> SvgRenderingFrame:
        """Pop segment render frame."""
        if len(self.rendering_stack) <= 1:
            raise RuntimeError
        return self.rendering_stack.pop()

    @property
    def frame(self) -> SvgRenderingFrame:
        """Get current rendering stack frame."""
        return self.rendering_stack[-1]

    def get_layer(self, polarity: Polarity) -> drawsvg.Group | drawsvg.Mask:
        """Get image layer."""
        if self.frame.polarity is None or polarity != self.frame.polarity:
            self.frame.polarity = polarity
            if polarity == Polarity.Dark:
                self._new_layer(with_mask=False)
            else:
                self._new_layer(with_mask=True)

        if self.frame.polarity == Polarity.Dark:
            return self.frame.layer

        return self.frame.mask

    def _new_layer(self, *, with_mask: bool) -> None:
        """Create new layer including previous layer."""
        if with_mask:
            self.frame.mask = self._make_mask(self.frame.bounding_box)
            new_layer = drawsvg.Group(mask=self.frame.mask)
        else:
            new_layer = drawsvg.Group()

        new_layer.append(self.frame.layer)

        self.frame.layer = new_layer

    def convert_x(self, x: Offset) -> Decimal:
        """Convert y offset to y coordinate in image space."""
        if self.frame.normalize_origin_to_0_0:
            origin_offset_x = self.frame.bounding_box.min_x.as_millimeters()
        else:
            origin_offset_x = Decimal(0)

        corrected_position_x = x.as_millimeters() - origin_offset_x

        return corrected_position_x * self.scale

    def convert_y(self, y: Offset) -> Decimal:
        """Convert y offset to y coordinate in image space."""
        return self._convert_y(
            y,
            normalize_origin_to_0_0=self.frame.normalize_origin_to_0_0,
            flip_y=self.frame.flip_y,
        )

    def _convert_y(
        self,
        y: Offset,
        *,
        normalize_origin_to_0_0: bool,
        flip_y: bool,
    ) -> Decimal:
        """Convert y offset to pixel y coordinate."""
        if normalize_origin_to_0_0:
            origin_offset_y = self.frame.bounding_box.min_y.as_millimeters()
        else:
            origin_offset_y = Decimal(0)

        corrected_position_y = y.as_millimeters() - origin_offset_y

        if flip_y:
            flipped_position_y = (
                self.frame.bounding_box.height.as_millimeters() - corrected_position_y
            )
            return flipped_position_y * self.scale
        return corrected_position_y * self.scale

    def convert_size(self, diameter: Offset) -> Decimal:
        """Convert y offset to pixel y coordinate."""
        return diameter.as_millimeters() * self.scale

    def get_color(self, polarity: Polarity) -> str:
        """Get color for specified polarity."""
        if self.frame.is_region:
            if polarity == Polarity.Dark:
                return self.color_scheme.solid_region_color.to_hex()
            return "black"

        if polarity == Polarity.Dark:
            return self.color_scheme.solid_color.to_hex()
        return "black"

    def get_aperture(self, aperture_id: int, color: str) -> Optional[drawsvg.Group]:
        """Get SVG group representing aperture."""
        return self.apertures.get(self._get_aperture_id(aperture_id, color))

    def _get_aperture_id(self, aperture_id: int, color: str) -> str:
        """Return combined ID for listed aperture."""
        return f"{color}+{aperture_id}"

    def set_aperture(
        self,
        aperture_id: int,
        color: str,
        aperture: drawsvg.Group,
    ) -> None:
        """Set SVG group representing aperture."""
        self.apertures[self._get_aperture_id(aperture_id, color)] = aperture

    def render_line(self, command: Line2) -> None:
        """Render line to target image."""
        color = self.get_color(command.transform.polarity)

        command.aperture.render_flash(
            self.renderer,
            Flash2(
                transform=command.transform,
                attributes=command.attributes,
                aperture=command.aperture,
                flash_point=command.start_point,
            ),
        )

        parallel_vector = command.start_point - command.end_point
        perpendicular_vector = parallel_vector.perpendicular()
        normalized_perpendicular_vector = perpendicular_vector.normalize()
        point_offset = normalized_perpendicular_vector * (
            command.aperture.get_stroke_width() / 2.0
        )

        p0 = command.start_point - point_offset
        p1 = command.start_point + point_offset
        p2 = command.end_point + point_offset
        p3 = command.end_point - point_offset

        rectangle = drawsvg.Lines(
            self.convert_x(p0.x),
            self.convert_y(p0.y),
            self.convert_x(p1.x),
            self.convert_y(p1.y),
            self.convert_x(p2.x),
            self.convert_y(p2.y),
            self.convert_x(p3.x),
            self.convert_y(p3.y),
            fill=color,
            close=True,
        )
        self.get_layer(command.transform.polarity).append(rectangle)

        command.aperture.render_flash(
            self.renderer,
            Flash2(
                transform=command.transform,
                attributes=command.attributes,
                aperture=command.aperture,
                flash_point=command.end_point,
            ),
        )

    def render_arc(self, command: Arc2) -> None:
        """Render arc to target image."""
        color = self.get_color(command.transform.polarity)
        # Arcs which start and end point overlaps are completely invisible in SVG.
        # Therefore we need to replace them with two half-full-arcs.
        # THB spec recommends doing it when exporting Gerber files, to avoid problems
        # with floating point numbers, but I guess nobody does that.
        if command.start_point == command.end_point:
            # This is a vector from center to start point, so we can invert it and
            # apply it twice to get the point on the opposite side of the center point.
            relative = command.get_relative_start_point()
            # Now we cen recursively invoke self with two modified copies of this
            # command.
            self.render_arc(
                command.model_copy(
                    update={
                        "start_point": command.start_point,
                        "end_point": command.start_point - (relative * 2),
                    },
                ),
            )
            self.render_arc(
                command.model_copy(
                    update={
                        "start_point": command.start_point - (relative * 2),
                        "end_point": command.start_point,
                    },
                ),
            )
            return

        command.aperture.render_flash(
            self.renderer,
            Flash2(
                transform=command.transform,
                attributes=command.attributes,
                aperture=command.aperture,
                flash_point=command.start_point,
            ),
        )
        # First we calculate perpendicular vector. This vector is always pointing
        # from the center, thus it is perpendicular to arc.
        # Then we can normalize it and multiply by half of aperture diameter,
        # effectively giving us vector pointing to inner/outer edge of line.
        # We can ignore the fact that we don't know which point (inner/outer) we
        # have, as long as we get the same every time, then we can pair it with
        # corresponding vector made from end point and create single arc,
        # Then invert both vectors and draw second arc.
        start_perpendicular_vector = command.get_relative_start_point()
        start_normalized_perpendicular_vector = start_perpendicular_vector.normalize()
        start_point_offset = start_normalized_perpendicular_vector * (
            command.aperture.get_stroke_width() / 2.0
        )

        end_perpendicular_vector = command.get_relative_end_point()
        end_normalized_perpendicular_vector = end_perpendicular_vector.normalize()
        end_point_offset = end_normalized_perpendicular_vector * (
            command.aperture.get_stroke_width() / 2.0
        )

        arc_path = drawsvg.Path(fill=color)

        # Determine start point of inner arc.
        start_inner = command.start_point + start_point_offset
        end_inner = command.end_point + end_point_offset
        # Move path ptr to inner arc start point.
        arc_path.M(
            self.convert_x(start_inner.x),
            self.convert_y(start_inner.y),
        )
        self.render_arc_to_path(
            command.model_copy(
                update={
                    "start_point": start_inner,
                    "end_point": end_inner,
                },
            ),
            arc_path,
        )
        # Determine start point of outer arc.
        # This arc have to be in reverse direction, so we swap start/end points.
        start_outer = command.end_point - end_point_offset
        end_outer = command.start_point - start_point_offset
        # Draw line between end of inner arc and start of outer arc.
        arc_path.L(
            self.convert_x(start_outer.x),
            self.convert_y(start_outer.y),
        )
        self.render_cc_arc_to_path(
            CCArc2(
                transform=command.transform,
                attributes=command.attributes,
                aperture=command.aperture,
                start_point=start_outer,
                center_point=command.center_point,
                end_point=end_outer,
            ),
            arc_path,
        )
        # Close arc box by drawing line between end of outer arc and start of inner
        arc_path.Z()
        self.get_layer(command.transform.polarity).append(arc_path)

        command.aperture.render_flash(
            self.renderer,
            Flash2(
                transform=command.transform,
                attributes=command.attributes,
                aperture=command.aperture,
                flash_point=command.end_point,
            ),
        )

    def render_cc_arc(self, command: CCArc2) -> None:
        """Render arc to target image."""
        self.render_arc(
            command.model_copy(
                update={
                    "start_point": command.end_point,
                    "end_point": command.start_point,
                },
            ),
        )

    def render_flash_circle(self, command: Flash2, aperture: Circle2) -> None:
        """Render flash circle to target image."""
        color = self.get_color(command.transform.polarity)
        aperture_group = self.get_aperture(id(aperture), color)

        if aperture_group is None:
            mask = self._make_mask(aperture.get_bounding_box(), aperture.hole_diameter)
            aperture_group = drawsvg.Group(mask=mask)
            aperture_group.append(
                drawsvg.Circle(
                    cx=0,
                    cy=0,
                    r=self.convert_size(aperture.diameter) / Decimal("2.0"),
                    fill=color,
                ),
            )
            self.set_aperture(id(aperture), color, aperture_group)

        self.get_layer(command.transform.polarity).append(
            drawsvg.Use(
                aperture_group,
                x=self.convert_x(command.flash_point.x),
                y=self.convert_y(command.flash_point.y),
            ),
        )

    def _make_mask(
        self,
        bbox: BoundingBox,
        hole_diameter: Optional[Offset] = None,
    ) -> drawsvg.Mask:
        mask = drawsvg.Mask()
        mask.append(
            drawsvg.Rectangle(
                x=self.convert_size(bbox.min_x),
                y=self.convert_size(bbox.min_y),
                width=self.convert_size(bbox.width),
                height=self.convert_size(bbox.height),
                fill="white",
            ),
        )
        if hole_diameter is not None:
            central_circle = drawsvg.Circle(
                cx=0,
                cy=0,
                r=self.convert_size(hole_diameter) / 2,
                fill="black",
            )
            mask.append(central_circle)
        return mask

    def render_flash_no_circle(self, command: Flash2, aperture: NoCircle2) -> None:
        """Render flash no circle aperture to target image."""

    def render_flash_rectangle(self, command: Flash2, aperture: Rectangle2) -> None:
        """Render flash rectangle to target image."""
        color = self.get_color(command.transform.polarity)
        aperture_group = self.get_aperture(id(aperture), color)

        if aperture_group is None:
            mask = self._make_mask(aperture.get_bounding_box(), aperture.hole_diameter)
            aperture_group = drawsvg.Group(mask=mask)
            aperture_group.append(
                drawsvg.Rectangle(
                    -self.convert_size(aperture.x_size) / 2,
                    -self.convert_size(aperture.y_size) / 2,
                    self.convert_size(aperture.x_size),
                    self.convert_size(aperture.y_size),
                    fill=color,
                ),
            )
            self.set_aperture(id(aperture), color, aperture_group)

        self.get_layer(command.transform.polarity).append(
            drawsvg.Use(
                aperture_group,
                self.convert_x(command.flash_point.x),
                self.convert_y(command.flash_point.y),
            ),
        )

    def render_flash_obround(self, command: Flash2, aperture: Obround2) -> None:
        """Render flash obround to target image."""
        color = self.get_color(command.transform.polarity)
        aperture_group = self.get_aperture(id(aperture), color)

        if aperture_group is None:
            mask = self._make_mask(aperture.get_bounding_box(), aperture.hole_diameter)
            aperture_group = drawsvg.Group(mask=mask)
            x_size = self.convert_size(aperture.x_size)
            y_size = self.convert_size(aperture.y_size)
            radius = x_size.min(y_size) / Decimal("2.0")

            aperture_group.append(
                drawsvg.Rectangle(
                    -self.convert_size(aperture.x_size) / 2,
                    -self.convert_size(aperture.y_size) / 2,
                    x_size,
                    y_size,
                    fill=color,
                    rx=radius,
                    ry=radius,
                ),
            )
            self.set_aperture(id(aperture), color, aperture_group)

        self.get_layer(command.transform.polarity).append(
            drawsvg.Use(
                aperture_group,
                self.convert_x(command.flash_point.x),
                self.convert_y(command.flash_point.y),
            ),
        )

    def render_flash_polygon(self, command: Flash2, aperture: Polygon2) -> None:
        """Render flash polygon to target image."""
        color = self.get_color(command.transform.polarity)
        aperture_group = self.get_aperture(id(aperture), color)

        if aperture_group is None:
            mask = self._make_mask(aperture.get_bounding_box(), aperture.hole_diameter)
            aperture_group = drawsvg.Group(mask=mask)

            number_of_vertices = aperture.number_vertices
            initial_angle = aperture.rotation
            inner_angle = Decimal("360") / Decimal(number_of_vertices)

            radius_vector = Vector2D.UNIT_X * (aperture.outer_diameter / Decimal("2.0"))
            rotated_radius_vector = radius_vector.rotate_around_origin(initial_angle)

            p = drawsvg.Path(fill=color)
            p.M(
                self.convert_size(rotated_radius_vector.x),
                self.convert_size(rotated_radius_vector.y),
            )

            for i in range(1, number_of_vertices):
                rotation_angle = inner_angle * i + initial_angle
                rotated_radius_vector = radius_vector.rotate_around_origin(
                    rotation_angle,
                )
                p.L(
                    self.convert_size(rotated_radius_vector.x),
                    self.convert_size(rotated_radius_vector.y),
                )

            p.Z()

            aperture_group.append(p)
            self.set_aperture(id(aperture), color, aperture_group)

        self.get_layer(command.transform.polarity).append(
            drawsvg.Use(
                aperture_group,
                self.convert_x(command.flash_point.x),
                self.convert_y(command.flash_point.y),
            ),
        )

    def render_flash_macro(self, command: Flash2, aperture: Macro2) -> None:
        """Render flash macro aperture to target image."""
        color = self.get_color(command.transform.polarity)
        aperture_group = self.get_aperture(id(aperture), color)

        if aperture_group is None:
            self.push_render_frame(
                aperture.command_buffer,
                normalize_origin_to_0_0=False,
                flip_y=False,
            )
            for cmd in aperture.command_buffer:
                cmd.render(self.renderer)

            frame = self.pop_render_frame()
            aperture_group = frame.layer
            self.set_aperture(id(aperture), color, aperture_group)

        self.get_layer(command.transform.polarity).append(
            drawsvg.Use(
                aperture_group,
                x=self.convert_x(command.flash_point.x),
                y=self.convert_y(command.flash_point.y),
            ),
        )

    def render_buffer(self, command: BufferCommand2) -> None:
        """Render buffer command, performing no writes."""
        for cmd in command:
            cmd.render(self.renderer)

    def render_region(self, command: Region2) -> None:
        """Render region to target image."""
        if len(command.command_buffer) == 0:
            return

        self.frame.is_region = True

        color = self.get_color(command.transform.polarity)
        region = drawsvg.Path(fill=color)

        for cmd in command.command_buffer:
            if isinstance(cmd, (Line2, Arc2, CCArc2)):
                region.M(
                    self.convert_x(cmd.start_point.x),
                    self.convert_y(cmd.start_point.y),
                )
                break

        for cmd in command.command_buffer:
            if isinstance(cmd, Line2):
                self.render_line_to_path(cmd, region)
            elif isinstance(cmd, Arc2):
                self.render_arc_to_path(cmd, region)
            elif isinstance(cmd, CCArc2):
                self.render_cc_arc_to_path(cmd, region)
            else:
                raise NotImplementedError

        region.Z()
        self.get_layer(command.transform.polarity).append(region)

        self.frame.is_region = False

    def render_line_to_path(self, command: Line2, path: drawsvg.Path) -> None:
        """Render line region boundary."""
        path.L(
            self.convert_x(command.end_point.x),
            self.convert_y(command.end_point.y),
        )

    def render_arc_to_path(self, command: Arc2, path: drawsvg.Path) -> None:
        """Render line region boundary."""
        relative_start_vector = command.get_relative_start_point()
        relative_end_vector = command.get_relative_end_point()

        angle_clockwise = relative_start_vector.angle_between(relative_end_vector)
        angle_counter_clockwise = relative_start_vector.angle_between_cc(
            relative_end_vector,
        )
        # We want to render clockwise angle, so if cc angle is bigger, we need to
        # choose small angle.
        large_arc = angle_clockwise >= angle_counter_clockwise
        sweep = 1

        path.A(
            rx=self.convert_size(command.get_radius()),
            ry=self.convert_size(command.get_radius()),
            ex=self.convert_x(command.end_point.x),
            ey=self.convert_y(command.end_point.y),
            rot=0,
            large_arc=large_arc,
            sweep=sweep,
        )

    def render_cc_arc_to_path(self, command: CCArc2, path: drawsvg.Path) -> None:
        """Render line region boundary."""
        relative_start_vector = command.get_relative_start_point()
        relative_end_vector = command.get_relative_end_point()

        angle_clockwise = relative_start_vector.angle_between(relative_end_vector)
        angle_counter_clockwise = relative_start_vector.angle_between_cc(
            relative_end_vector,
        )
        # We want to render clockwise angle, so if cc angle is bigger, we need to
        # choose small angle.
        large_arc = not (angle_clockwise >= angle_counter_clockwise)
        sweep = 0

        path.A(
            rx=self.convert_size(command.get_radius()),
            ry=self.convert_size(command.get_radius()),
            ex=self.convert_x(command.end_point.x),
            ey=self.convert_y(command.end_point.y),
            rot=0,
            large_arc=large_arc,
            sweep=sweep,
        )

    def get_image_ref(self) -> ImageRef:
        """Get reference to render image."""
        return SvgImageRef(self.drawing)

    def finalize(self) -> None:
        """Finalize rendering."""
        if len(self.rendering_stack) > 1:
            self.rendering_stack = [self.rendering_stack[0]]
        elif len(self.rendering_stack) < 1:
            raise RuntimeError

        width = self.convert_size(self.frame.bounding_box.width)
        height = self.convert_size(self.frame.bounding_box.height)
        self.drawing = drawsvg.Drawing(
            width=width,
            height=height,
        )
        self.drawing.append(self.get_layer(Polarity.Dark))


class SvgImageRef(ImageRef):
    """Generic container for reference to rendered image."""

    def __init__(self, image: drawsvg.Drawing) -> None:
        self.image = image

    def _save_to_io(
        self,
        output: BinaryIO,
        options: Optional[FormatOptions] = None,  # noqa: ARG002
    ) -> None:
        """Save rendered image to bytes stream buffer."""
        svg = self.image.as_svg()
        if svg is None:
            return
        output.write(svg.encode("utf-8"))


class SvgFormatOptions:
    """Format options for SVG format."""
