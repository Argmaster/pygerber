"""Module contains implementation of Gerber rendering backend outputting raster
images.
"""

from __future__ import annotations

import math
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, BinaryIO, Optional

from PIL import Image, ImageDraw

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
from pygerber.gerberx3.state_enums import Polarity

if TYPE_CHECKING:
    from typing_extensions import Self


class RasterRenderer2(Renderer2):
    """Rendering backend for creating raster images."""

    def __init__(
        self,
        hooks: Optional[RasterRenderer2Hooks] = None,
    ) -> None:
        hooks = RasterRenderer2Hooks() if hooks is None else hooks
        super().__init__(hooks)


class RasterRenderingFrameBuilder:
    """Builder for RasterRenderingFrame."""

    def __init__(
        self,
        command_buffer: ReadonlyCommandBuffer2,
    ) -> None:
        self.command_buffer = command_buffer
        self.bounding_box: Optional[BoundingBox] = None
        self.image: Optional[Image.Image] = None
        self.mask: Optional[Image.Image] = None
        self.polarity: Optional[Polarity] = None
        self.is_region: bool = False
        self.dpmm = 1
        self.scale = Decimal("1")

    def set_dpmm(self, dpmm: int) -> Self:
        """Specify image dpmm."""
        self.dpmm = dpmm
        return self

    def set_scale(self, scale: Decimal) -> Self:
        """Specify rendering scale."""
        self.scale = scale
        return self

    def set_bounding_box(self, bounding_box: BoundingBox) -> Self:
        """Specify bounding box."""
        self.bounding_box = bounding_box
        return self

    def set_image(self, image: Image.Image) -> Self:
        """Specify image."""
        self.image = image
        return self

    def set_mask(self, mask: Image.Image) -> Self:
        """Specify mask."""
        self.mask = mask
        return self

    def set_polarity(self, polarity: Optional[Polarity]) -> Self:
        """Specify polarity."""
        self.polarity = polarity
        return self

    def set_region(self, *, is_region: bool) -> Self:
        """Specify region."""
        self.is_region = is_region
        return self

    def build(self) -> RasterRenderingFrame:
        """Build final rendering frame container."""
        bbox = (
            self.command_buffer.get_bounding_box()
            if self.bounding_box is None
            else self.bounding_box
        )
        dimensions = (
            max(int(bbox.width.as_millimeters() * self.dpmm * self.scale), 1),
            max(int(bbox.height.as_millimeters() * self.dpmm * self.scale), 1),
        )
        image = (
            Image.new("RGBA", dimensions, (0, 0, 0, 0))
            if self.image is None
            else self.image
        )
        mask = (
            Image.new("RGBA", dimensions, (0, 0, 0, 0))
            if self.mask is None
            else self.mask
        )
        return RasterRenderingFrame(
            command_buffer=self.command_buffer,
            bounding_box=bbox,
            image=image,
            layer=ImageDraw.ImageDraw(image),
            mask=mask,
            mask_draw=ImageDraw.ImageDraw(mask),
            polarity=self.polarity,
            is_region=self.is_region,
        )


class RasterRenderingFrame:
    """Container for rendering variables."""

    def __init__(  # noqa: PLR0913
        self,
        command_buffer: ReadonlyCommandBuffer2,
        bounding_box: BoundingBox,
        image: Image.Image,
        layer: ImageDraw.ImageDraw,
        mask: Image.Image,
        mask_draw: ImageDraw.ImageDraw,
        polarity: Optional[Polarity] = None,
        *,
        is_region: bool = False,
    ) -> None:
        self.command_buffer = command_buffer
        self.bounding_box = bounding_box
        self.image = image
        self.layer = layer
        self.mask = mask
        self.mask_draw = mask_draw
        self.layer = layer
        self.polarity = polarity
        self.is_region = is_region

    def get_aperture(self) -> RasterAperture:
        """Return aperture."""
        return RasterAperture(image=self.image, mask=self.mask)


class RasterAperture:
    """Raster Aperture model."""

    def __init__(self, image: Image.Image, mask: Image.Image) -> None:
        self.image = image
        self.mask = mask


class RasterRenderer2Hooks(Renderer2HooksABC):
    """Class implementing rendering hooks to output raster images."""

    def __init__(
        self,
        color_scheme: ColorScheme = ColorScheme.DEBUG_1_ALPHA,
        scale: Decimal = Decimal("1"),
        dpmm: int = 20,
        *,
        flip_y: bool = True,
    ) -> None:
        self.color_scheme = color_scheme
        self.scale = scale
        self.dpmm = dpmm
        self.flip_y = flip_y

    def init(
        self,
        renderer: Renderer2,
        command_buffer: ReadonlyCommandBuffer2,
    ) -> None:
        """Initialize renderer."""
        if not isinstance(renderer, RasterRenderer2):
            raise NotImplementedError

        self.renderer = renderer
        self.command_buffer = command_buffer
        self.rendering_stack: list[RasterRenderingFrame] = []
        self.push_render_frame(
            RasterRenderingFrameBuilder(command_buffer=self.command_buffer)
            .set_dpmm(self.dpmm)
            .set_scale(self.scale)
            .build(),
        )
        self.apertures: dict[str, RasterAperture] = {}

    def push_render_frame(self, cmd: RasterRenderingFrame) -> None:
        """Push new segment render frame."""
        self.rendering_stack.append(cmd)

    def pop_render_frame(self) -> RasterRenderingFrame:
        """Pop segment render frame."""
        if len(self.rendering_stack) <= 1:
            raise RuntimeError
        return self.rendering_stack.pop()

    @property
    def frame(self) -> RasterRenderingFrame:
        """Get current rendering stack frame."""
        return self.rendering_stack[-1]

    def get_layer(self) -> ImageDraw.ImageDraw:
        """Get image layer."""
        return self.frame.layer

    def get_image(self) -> Image.Image:
        """Get image layer."""
        return self.frame.image

    def get_mask(self) -> Image.Image:
        """Get mask layer."""
        return self.frame.mask

    def get_mask_draw(self) -> ImageDraw.ImageDraw:
        """Get mask layer."""
        return self.frame.mask_draw

    def convert_x(self, x: Offset) -> int:
        """Convert y offset to y coordinate in image space."""
        origin_offset_x = self.frame.bounding_box.min_x.as_millimeters()
        corrected_position_x = x.as_millimeters() - origin_offset_x
        return int(corrected_position_x * self.scale * self.dpmm)

    def convert_y(self, y: Offset) -> int:
        """Convert y offset to y coordinate in image space."""
        origin_offset_y = self.frame.bounding_box.min_y.as_millimeters()
        corrected_position_y = y.as_millimeters() - origin_offset_y
        return int(corrected_position_y * self.scale * self.dpmm)

    def convert_size(self, diameter: Offset) -> int:
        """Convert y offset to pixel y coordinate."""
        return int(diameter.as_millimeters() * self.scale * self.dpmm)

    def convert_bbox(self, bbox: BoundingBox) -> tuple[int, int, int, int]:
        """Convert bounding box region to pixel coordinates bbox."""
        return (
            self.convert_x(bbox.min_x),
            self.convert_y(bbox.min_y),
            self.convert_x(bbox.max_x),
            self.convert_y(bbox.max_y),
        )

    def get_color(self, polarity: Polarity) -> str:
        """Get color for specified polarity."""
        if self.frame.is_region:
            if polarity == Polarity.Dark:
                return self.color_scheme.solid_region_color.to_hex()
            return self.color_scheme.clear_region_color.to_hex()

        if polarity == Polarity.Dark:
            return self.color_scheme.solid_color.to_hex()
        return self.color_scheme.clear_color.to_hex()

    def get_mask_color(self, polarity: Polarity) -> str:
        """Get color for specified polarity."""
        if polarity == Polarity.Dark:
            return "#FFFFFFFF"
        return "#000000FF"

    def get_aperture(self, aperture_id: int, color: str) -> Optional[RasterAperture]:
        """Get SVG group representing aperture."""
        return self.apertures.get(self._get_aperture_id(aperture_id, color))

    def set_aperture(
        self,
        aperture_id: int,
        color: str,
        aperture: RasterAperture,
    ) -> None:
        """Set SVG group representing aperture."""
        self.apertures[self._get_aperture_id(aperture_id, color)] = aperture

    def _get_aperture_id(self, aperture_id: int, color: str) -> str:
        """Return combined ID for listed aperture."""
        return f"{color}+{aperture_id}"

    def render_line(self, command: Line2) -> None:
        """Render line to target image."""
        command.aperture.render_flash(
            self.renderer,
            Flash2(
                transform=command.transform,
                attributes=command.attributes,
                aperture=command.aperture,
                flash_point=command.start_point,
            ),
        )

        for img, color in (
            (self.get_layer(), self.get_color(command.transform.polarity)),
            (
                self.get_mask_draw(),
                self.get_mask_color(command.transform.polarity),
            ),
        ):
            img.line(
                (
                    self.convert_x(command.start_point.x),
                    self.convert_y(command.start_point.y),
                    self.convert_x(command.end_point.x),
                    self.convert_y(command.end_point.y),
                ),
                width=self.convert_size(command.aperture.get_stroke_width()),
                fill=color,
            )

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
        command.aperture.render_flash(
            self.renderer,
            Flash2(
                transform=command.transform,
                attributes=command.attributes,
                aperture=command.aperture,
                flash_point=command.start_point,
            ),
        )

        start_angle = (
            command.get_relative_start_point().angle_between(
                Vector2D.UNIT_X,
            )
            % 360
        )
        end_angle = (
            command.get_relative_end_point().angle_between(
                Vector2D.UNIT_X,
            )
            % 360
        )
        bbox = self.convert_bbox(
            BoundingBox.from_diameter(
                (command.get_radius() * 2) + (command.aperture.get_stroke_width()),
            )
            + command.center_point,
        )

        if end_angle <= start_angle:
            end_angle += 360

        for img, color in (
            (self.get_layer(), self.get_color(command.transform.polarity)),
            (
                self.get_mask_draw(),
                self.get_mask_color(command.transform.polarity),
            ),
        ):
            img.arc(
                bbox,
                start_angle,
                end_angle,
                fill=color,
                width=self.convert_size(command.aperture.get_stroke_width()),
            )

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
        return self.render_arc(
            command.model_copy(
                update={
                    "start_point": command.start_point,
                    "end_point": command.end_point,
                },
            ),
        )

    def render_flash_circle(self, command: Flash2, aperture: Circle2) -> None:
        """Render flash circle to target image."""
        aperture_color = self.get_color(command.transform.polarity)
        aperture_image = self.get_aperture(id(aperture), aperture_color)

        if aperture_image is None:
            self.push_render_frame(
                RasterRenderingFrameBuilder(ReadonlyCommandBuffer2(commands=[command]))
                .set_dpmm(self.dpmm)
                .set_scale(self.scale)
                .build(),
            )

            for img, fill_color in (
                (self.get_layer(), self.get_color(command.transform.polarity)),
                (
                    self.get_mask_draw(),
                    self.get_mask_color(command.transform.polarity),
                ),
            ):
                img.ellipse(
                    self.convert_bbox(command.get_bounding_box()),
                    fill=fill_color,
                )

            frame = self.pop_render_frame()
            aperture_image = frame.get_aperture()
            self.set_aperture(id(aperture), aperture_color, aperture_image)

        self._paste_aperture(command, aperture_image)

    def _paste_aperture(self, command: Flash2, aperture_image: RasterAperture) -> None:
        bbox = command.get_bounding_box()
        origin_x, origin_y = self.convert_bbox(bbox)[0:2]
        self.get_image().paste(
            aperture_image.image,
            (origin_x + 1, origin_y + 1),
            mask=aperture_image.mask,
        )

    def render_flash_no_circle(self, command: Flash2, aperture: NoCircle2) -> None:
        """Render flash no circle aperture to target image."""

    def render_flash_rectangle(self, command: Flash2, aperture: Rectangle2) -> None:
        """Render flash rectangle to target image."""
        color = self.get_color(command.transform.polarity)
        aperture_image = self.get_aperture(id(aperture), color)

        if aperture_image is None:
            self.push_render_frame(
                RasterRenderingFrameBuilder(ReadonlyCommandBuffer2(commands=[command]))
                .set_dpmm(self.dpmm)
                .set_scale(self.scale)
                .build(),
            )

            for img, fill_color in (
                (self.get_layer(), self.get_color(command.transform.polarity)),
                (
                    self.get_mask_draw(),
                    self.get_mask_color(command.transform.polarity),
                ),
            ):
                img.rectangle(
                    self.convert_bbox(command.get_bounding_box()),
                    fill=fill_color,
                )

            frame = self.pop_render_frame()
            aperture_image = frame.get_aperture()
            self.set_aperture(id(aperture), color, aperture_image)

        self._paste_aperture(command, aperture_image)

    def render_flash_obround(self, command: Flash2, aperture: Obround2) -> None:
        """Render flash obround to target image."""
        color = self.get_color(command.transform.polarity)
        aperture_image = self.get_aperture(id(aperture), color)

        if aperture_image is None:
            self.push_render_frame(
                RasterRenderingFrameBuilder(ReadonlyCommandBuffer2(commands=[command]))
                .set_dpmm(self.dpmm)
                .set_scale(self.scale)
                .build(),
            )
            for img, fill_color in (
                (self.get_layer(), self.get_color(command.transform.polarity)),
                (
                    self.get_mask_draw(),
                    self.get_mask_color(command.transform.polarity),
                ),
            ):
                img.rounded_rectangle(
                    self.convert_bbox(command.get_bounding_box()),
                    radius=min(
                        self.convert_size(aperture.x_size),
                        self.convert_size(aperture.y_size),
                    )
                    // 2,
                    fill=fill_color,
                )
            frame = self.pop_render_frame()
            aperture_image = frame.get_aperture()
            self.set_aperture(id(aperture), color, aperture_image)

        self._paste_aperture(command, aperture_image)

    def render_flash_polygon(self, command: Flash2, aperture: Polygon2) -> None:
        """Render flash polygon to target image."""
        color = self.get_color(command.transform.polarity)
        aperture_image = self.get_aperture(id(aperture), color)

        if aperture_image is None:
            self.push_render_frame(
                RasterRenderingFrameBuilder(ReadonlyCommandBuffer2(commands=[command]))
                .set_dpmm(self.dpmm)
                .set_scale(self.scale)
                .build(),
            )

            outer_diameter = self.convert_size(aperture.outer_diameter)
            radius = outer_diameter // 2
            # In PIL rotation angle goes in opposite direction than in Gerber and
            # starts from different orientation.
            rotation = -float(aperture.rotation) - 90.0
            bbox = command.get_bounding_box()

            for img, fill_color in (
                (self.get_layer(), self.get_color(command.transform.polarity)),
                (
                    self.get_mask_draw(),
                    self.get_mask_color(command.transform.polarity),
                ),
            ):
                img.regular_polygon(
                    (
                        self.convert_x(bbox.min_x) + radius,
                        self.convert_y(bbox.min_y) + radius,
                        radius,
                    ),
                    n_sides=aperture.number_vertices,
                    rotation=rotation,
                    fill=fill_color,
                )

            frame = self.pop_render_frame()
            aperture_image = frame.get_aperture()
            self.set_aperture(id(aperture), color, aperture_image)

        self._paste_aperture(command, aperture_image)

    def render_flash_macro(self, command: Flash2, aperture: Macro2) -> None:
        """Render flash macro aperture to target image."""
        color = self.get_color(command.transform.polarity)
        aperture_image = self.get_aperture(id(aperture), color)

        if aperture_image is None:
            self.push_render_frame(
                RasterRenderingFrameBuilder(ReadonlyCommandBuffer2(commands=[command]))
                .set_dpmm(self.dpmm)
                .set_scale(self.scale)
                .build(),
            )

            for cmd in aperture.command_buffer:
                cmd.render(self.renderer)

            frame = self.pop_render_frame()
            aperture_image = frame.get_aperture()
            self.set_aperture(id(aperture), color, aperture_image)

        self._paste_aperture(command, aperture_image)

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
        points: list[tuple[int, int]] = []

        for cmd in command.command_buffer:
            if isinstance(cmd, Line2):
                self.generate_line_points(cmd, points)
            elif isinstance(cmd, Arc2):
                self.generate_arc_points(cmd, points)
            elif isinstance(cmd, CCArc2):
                self.generate_cc_arc_points(cmd, points)
            else:
                raise NotImplementedError

        self.get_layer().polygon(points, fill=color)

    def generate_line_points(
        self,
        command: Line2,
        points: list[tuple[int, int]],
    ) -> None:
        """Generate points of line region boundary."""
        points.append(
            (
                self.convert_x(command.start_point.x),
                self.convert_y(command.start_point.y),
            ),
        )
        points.append(
            (
                self.convert_x(command.end_point.x),
                self.convert_y(command.end_point.y),
            ),
        )

    def generate_arc_points(self, command: Arc2, points: list[tuple[int, int]]) -> None:
        """Generate points of arc region boundary."""
        points.append(
            (
                self.convert_x(command.start_point.x),
                self.convert_y(command.start_point.y),
            ),
        )
        angle = command.get_relative_start_point().angle_between(
            command.get_relative_end_point(),
        )
        angle_ratio = angle / 360
        arc_length = (command.get_radius() * 2 * math.pi) * angle_ratio
        point_count = self.convert_size(arc_length) // 10
        angle_step = Decimal(angle) / Decimal(point_count)

        current_point = command.get_relative_start_point()
        for i in range(point_count - 1):
            rotated_current_point = current_point.rotate_around_origin(
                -(i * angle_step),
            )
            absolute_current_point = command.center_point + rotated_current_point
            points.append(
                (
                    self.convert_x(absolute_current_point.x),
                    self.convert_y(absolute_current_point.y),
                ),
            )

        points.append(
            (
                self.convert_x(command.end_point.x),
                self.convert_y(command.end_point.y),
            ),
        )

    def generate_cc_arc_points(
        self,
        command: CCArc2,
        points: list[tuple[int, int]],
    ) -> None:
        """Generate points of counter clockwise arc region boundary."""
        points.append(
            (
                self.convert_x(command.start_point.x),
                self.convert_y(command.start_point.y),
            ),
        )
        angle = command.get_relative_start_point().angle_between(
            command.get_relative_end_point(),
        )
        angle_ratio = angle / 360
        arc_length = (command.get_radius() * 2 * math.pi) * angle_ratio
        point_count = self.convert_size(arc_length) // 10
        angle_step = Decimal(angle) / Decimal(point_count)

        current_point = command.get_relative_start_point()
        for i in range(point_count - 1):
            rotated_current_point = current_point.rotate_around_origin(i * angle_step)
            absolute_current_point = command.center_point + rotated_current_point
            points.append(
                (
                    self.convert_x(absolute_current_point.x),
                    self.convert_y(absolute_current_point.y),
                ),
            )

        points.append(
            (
                self.convert_x(command.end_point.x),
                self.convert_y(command.end_point.y),
            ),
        )

    def finalize(self) -> None:
        """Finalize renderer."""

    def get_image_ref(self) -> ImageRef:
        """Get reference to render image."""
        return RasterImageRef(self.frame.image)


class RasterImageRef(ImageRef):
    """Reference to raster image."""

    def __init__(self, image: Image.Image) -> None:
        self.image = image

    def _save_to_io(
        self,
        output: BinaryIO,
        options: FormatOptions | None = None,
    ) -> None:
        if isinstance(options, RasterFormatOptions):
            if self.image.mode != options.pixel_format.value:
                image = self.image.convert(options.pixel_format.value)
            else:
                image = self.image

            image.save(output, format=options.image_format.value)
            return

        self.image.save(output)

    def get_image(self) -> Image.Image:
        """Get image reference."""
        return self.image


class ImageFormat(Enum):
    """List of officially supported raster image formats."""

    PNG = "png"
    JPEG = "jpg"


class PixelFormat(Enum):
    """List of officially supported pixel formats."""

    RGB = "RGB"
    RGBA = "RGBA"


class RasterFormatOptions:
    """Raster Format specific options."""

    def __init__(
        self,
        image_format: ImageFormat = ImageFormat.PNG,
        pixel_format: PixelFormat = PixelFormat.RGBA,
    ) -> None:
        self.image_format = image_format
        self.pixel_format = pixel_format
