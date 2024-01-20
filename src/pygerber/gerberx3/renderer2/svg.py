"""Module contains implementation of Gerber rendering backend outputting SVG files."""
from __future__ import annotations

import importlib.util
from decimal import Decimal
from typing import BinaryIO, Optional

from pygerber.backend.rasterized_2d.color_scheme import ColorScheme
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.apertures2.block2 import Block2
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
        color_scheme: ColorScheme = ColorScheme.DEBUG_1,
    ) -> None:
        hooks = SvgRenderer2Hooks() if hooks is None else hooks
        self.color_scheme = color_scheme
        super().__init__(hooks)


class SvgRenderer2Hooks(Renderer2HooksABC):
    """Rendering backend hooks used to render SVG images."""

    renderer: SvgRenderer2

    def init(
        self,
        renderer: Renderer2,
        command_buffer: ReadonlyCommandBuffer2,
    ) -> None:
        """Initialize rendering."""
        if not isinstance(renderer, SvgRenderer2):
            raise NotImplementedError

        self.renderer = renderer
        self.command_buffer = command_buffer
        self.bounding_box = self.command_buffer.get_bounding_box()
        self.color_scheme = self.renderer.color_scheme

        self.mask = drawsvg.Mask()
        self.layer = drawsvg.Group()
        self.current_polarity: Optional[Polarity] = None

        self.region_point_buffer: list[Decimal] = []
        self.is_region: bool = False
        self.scale = Decimal("10")

        self.apertures: dict[str, drawsvg.Group] = {}

    def get_layer(self, polarity: Polarity) -> drawsvg.Group | drawsvg.Mask:
        """Get image layer."""
        if self.current_polarity is None or polarity != self.current_polarity:
            self.current_polarity = polarity
            new_mask = drawsvg.Mask()
            # Add solid background for mask to not mask anything by default.
            # Following writes to mask will be black to hide parts of the mask.
            new_mask.append(
                drawsvg.Rectangle(
                    self.bounding_box.min_x.as_millimeters(),
                    self.bounding_box.min_y.as_millimeters(),
                    self.bounding_box.width.as_millimeters(),
                    self.bounding_box.height.as_millimeters(),
                    fill="white",
                ),
            )
            new_layer = drawsvg.Group(mask=new_mask)
            new_layer.append(self.layer)

            self.layer = new_layer
            self.mask = new_mask

        if self.current_polarity == Polarity.Dark:
            return self.layer

        return self.mask

    def get_color(self, polarity: Polarity) -> str:
        """Get color for specified polarity."""
        if self.is_region:
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

    def render_buffer(self, command: BufferCommand2) -> None:
        """Render command buffer to target image."""

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
            p0.x.as_millimeters(),
            p0.y.as_millimeters(),
            p1.x.as_millimeters(),
            p1.y.as_millimeters(),
            p2.x.as_millimeters(),
            p2.y.as_millimeters(),
            p3.x.as_millimeters(),
            p3.y.as_millimeters(),
            fill=color,
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

    def render_cc_arc(self, command: Arc2) -> None:
        """Render arc to target image."""

    def render_flash_circle(self, command: Flash2, aperture: Circle2) -> None:
        """Render flash circle to target image."""
        color = self.get_color(command.transform.polarity)
        aperture_group = self.get_aperture(id(aperture), color)

        if aperture_group is None:
            aperture_group = drawsvg.Group()
            aperture_group.append(
                drawsvg.Circle(
                    0,
                    0,
                    aperture.diameter.as_millimeters() / Decimal("2.0"),
                    fill=color,
                ),
            )
            self.set_aperture(id(aperture), color, aperture_group)

        self.get_layer(command.transform.polarity).append(
            drawsvg.Use(
                aperture_group,
                command.flash_point.x.as_millimeters(),
                command.flash_point.y.as_millimeters(),
            ),
        )

    def render_flash_no_circle(self, command: Flash2, aperture: NoCircle2) -> None:
        """Render flash no circle aperture to target image."""

    def render_flash_rectangle(self, command: Flash2, aperture: Rectangle2) -> None:
        """Render flash rectangle to target image."""
        color = self.get_color(command.transform.polarity)
        aperture_group = self.get_aperture(id(aperture), color)

        x_size = aperture.x_size.as_millimeters()
        y_size = aperture.y_size.as_millimeters()

        if aperture_group is None:
            aperture_group = drawsvg.Group()
            aperture_group.append(
                drawsvg.Rectangle(
                    Decimal("0.0"),
                    Decimal("0.0"),
                    x_size,
                    y_size,
                    fill=color,
                ),
            )
            self.set_aperture(id(aperture), color, aperture_group)

        self.get_layer(command.transform.polarity).append(
            drawsvg.Use(
                aperture_group,
                command.flash_point.x.as_millimeters() - (x_size / Decimal("2.0")),
                command.flash_point.y.as_millimeters() - (y_size / Decimal("2.0")),
            ),
        )

    def render_flash_obround(self, command: Flash2, aperture: Obround2) -> None:
        """Render flash obround to target image."""
        color = self.get_color(command.transform.polarity)
        aperture_group = self.get_aperture(id(aperture), color)

        x_size = aperture.x_size.as_millimeters()
        y_size = aperture.y_size.as_millimeters()

        if aperture_group is None:
            aperture_group = drawsvg.Group()
            radius = x_size.min(y_size) / Decimal("2.0")
            aperture_group.append(
                drawsvg.Rectangle(
                    Decimal("0.0"),
                    Decimal("0.0"),
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
                command.flash_point.x.as_millimeters() - (x_size / Decimal("2.0")),
                command.flash_point.y.as_millimeters() - (y_size / Decimal("2.0")),
            ),
        )

    def render_flash_polygon(self, command: Flash2, aperture: Polygon2) -> None:
        """Render flash polygon to target image."""
        color = self.get_color(command.transform.polarity)
        aperture_group = self.get_aperture(id(aperture), color)

        outer_diameter = aperture.outer_diameter.as_millimeters()

        if aperture_group is None:
            aperture_group = drawsvg.Group()

            number_of_vertices = aperture.number_vertices
            initial_angle = aperture.rotation
            inner_angle = Decimal("360") / Decimal(number_of_vertices)
            radius_vector = Vector2D.UNIT_X * (outer_diameter / Decimal("2.0"))

            p = drawsvg.Path(fill=color)
            rotated_radius_vector = radius_vector.rotate_around_origin(initial_angle)
            p.M(
                rotated_radius_vector.x.as_millimeters(),
                rotated_radius_vector.y.as_millimeters(),
            )

            for i in range(1, number_of_vertices):
                rotation_angle = inner_angle * i + initial_angle
                rotated_radius_vector = radius_vector.rotate_around_origin(
                    rotation_angle,
                )
                p.L(
                    rotated_radius_vector.x.as_millimeters(),
                    rotated_radius_vector.y.as_millimeters(),
                )

            p.Z()

            aperture_group.append(p)
            self.set_aperture(id(aperture), color, aperture_group)

        self.get_layer(command.transform.polarity).append(
            drawsvg.Use(
                aperture_group,
                command.flash_point.x.as_millimeters(),
                command.flash_point.y.as_millimeters(),
            ),
        )

    def render_flash_macro(self, command: Flash2, aperture: Macro2) -> None:
        """Render flash macro aperture to target image."""

    def render_flash_block(self, command: Flash2, aperture: Block2) -> None:
        """Render flash block aperture to target image."""

    def render_region(self, command: Region2) -> None:
        """Render region to target image."""
        self.is_region = True
        self.region_point_buffer = []

        for cmd in command.command_buffer:
            if isinstance(cmd, Line2):
                self.render_region_line(cmd)
            elif isinstance(cmd, Arc2):
                self.render_region_arc(cmd)
            elif isinstance(cmd, CCArc2):
                self.render_region_cc_arc(cmd)
            else:
                raise NotImplementedError

        color = self.get_color(command.transform.polarity)

        region = drawsvg.Lines(
            *self.region_point_buffer,
            fill=color,
            close=True,
        )
        self.get_layer(command.transform.polarity).append(region)

        self.is_region = False
        self.region_point_buffer = []

    def render_region_line(self, command: Line2) -> None:
        """Render line region boundary."""
        self.region_point_buffer.append(command.start_point.x.as_millimeters())
        self.region_point_buffer.append(command.start_point.y.as_millimeters())
        self.region_point_buffer.append(command.end_point.x.as_millimeters())
        self.region_point_buffer.append(command.end_point.y.as_millimeters())

    def render_region_arc(self, command: Arc2) -> None:
        """Render line region boundary."""
        self.region_point_buffer.append(command.start_point.x.as_millimeters())
        self.region_point_buffer.append(command.start_point.y.as_millimeters())
        self.region_point_buffer.append(command.end_point.x.as_millimeters())
        self.region_point_buffer.append(command.end_point.y.as_millimeters())

    def render_region_cc_arc(self, command: CCArc2) -> None:
        """Render line region boundary."""
        self.region_point_buffer.append(command.start_point.x.as_millimeters())
        self.region_point_buffer.append(command.start_point.y.as_millimeters())
        self.region_point_buffer.append(command.end_point.x.as_millimeters())
        self.region_point_buffer.append(command.end_point.y.as_millimeters())

    def get_image_ref(self) -> ImageRef:
        """Get reference to render image."""
        return SvgImageRef(self.drawing)

    def finalize(self) -> None:
        """Finalize rendering."""
        width = self.bounding_box.width.as_millimeters()
        height = self.bounding_box.height.as_millimeters()
        self.drawing = drawsvg.Drawing(
            width=width,
            height=height,
            origin=(
                self.bounding_box.min_x.as_millimeters(),
                self.bounding_box.min_y.as_millimeters(),
            ),
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
