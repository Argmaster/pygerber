"""Module contains implementation of Gerber rendering backend outputting raster
images.
"""

from __future__ import annotations

import gc
import math
from contextlib import contextmanager
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Any, BinaryIO, ContextManager, Generator, Optional

from PIL import Image, ImageDraw

from pygerber.backend.rasterized_2d.color_scheme import ColorScheme
from pygerber.common.error import throw
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2
from pygerber.gerberx3.parser2.apertures2.circle2 import Circle2, NoCircle2
from pygerber.gerberx3.parser2.apertures2.macro2 import Macro2
from pygerber.gerberx3.parser2.apertures2.obround2 import Obround2
from pygerber.gerberx3.parser2.apertures2.polygon2 import Polygon2
from pygerber.gerberx3.parser2.apertures2.rectangle2 import Rectangle2
from pygerber.gerberx3.parser2.command_buffer2 import ReadonlyCommandBuffer2
from pygerber.gerberx3.parser2.commands2.arc2 import Arc2, CCArc2
from pygerber.gerberx3.parser2.commands2.command2 import Command2
from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
from pygerber.gerberx3.parser2.commands2.line2 import Line2
from pygerber.gerberx3.parser2.commands2.region2 import Region2
from pygerber.gerberx3.parser2.state2 import ApertureTransform
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


HALF = Decimal("0.5")


def custom_round(value: Decimal | float) -> int:
    """Round value to jason integer."""
    int_val = int(value)
    diff = abs(int_val - Decimal(value))

    if diff >= HALF:
        return int_val

    return int_val


class RasterRenderingFrameBuilder:
    """Builder for RasterRenderingFrame."""

    def __init__(self) -> None:
        self.command_buffer: Optional[ReadonlyCommandBuffer2] = None
        self.bounding_box: Optional[BoundingBox] = None
        self.image: Optional[Image.Image] = None
        self.mask: Optional[Image.Image] = None
        self.color_scheme: Optional[ColorScheme] = None
        self.is_region: bool = False
        self.dpmm = 1
        self.scale = Decimal("1")
        self.polarity: Optional[Polarity] = None
        self.x_offset = 0
        self.y_offset = 0

    def set_command_buffer(self, command_buffer: ReadonlyCommandBuffer2) -> Self:
        """Specify source buffer."""
        self.command_buffer = command_buffer
        return self

    def set_command_buffer_from_list(self, commands: list[Command2]) -> Self:
        """Specify source buffer."""
        self.command_buffer = ReadonlyCommandBuffer2(commands=commands)
        return self

    def set_dpmm(self, dpmm: int) -> Self:
        """Specify image dpmm."""
        self.dpmm = dpmm
        return self

    def set_scale(self, scale: Decimal) -> Self:
        """Specify rendering scale."""
        self.scale = scale
        return self

    def set_image(self, image: Image.Image) -> Self:
        """Specify image."""
        self.image = image
        return self

    def set_mask(self, mask: Image.Image) -> Self:
        """Specify mask."""
        self.mask = mask
        return self

    def set_region(self, *, is_region: bool) -> Self:
        """Specify region."""
        self.is_region = is_region
        return self

    def set_color_scheme(self, color_scheme: ColorScheme) -> Self:
        """Specify color scheme."""
        self.color_scheme = color_scheme
        return self

    def set_polarity(self, polarity: Polarity) -> Self:
        """Specify polarity."""
        self.polarity = polarity
        return self

    def set_pixel_dimension_offsets(self, x: int = 0, y: int = 0) -> Self:
        """Set pixel dimension offsets."""
        self.x_offset = x
        self.y_offset = y
        return self

    def build(self, *, with_mask: bool = True) -> RasterRenderingFrame:
        """Build final rendering frame container."""
        command_buffer = (
            self.command_buffer
            if self.command_buffer is not None
            else throw(RuntimeError("Command buffer not set."))
        )
        bbox = (
            command_buffer.get_bounding_box()
            if self.bounding_box is None
            else self.bounding_box
        )
        dimensions = (
            max(custom_round(bbox.width.as_millimeters() * self.dpmm * self.scale), 1)
            + self.x_offset,
            max(custom_round(bbox.height.as_millimeters() * self.dpmm * self.scale), 1)
            + self.y_offset,
        )
        image = (
            Image.new("RGBA", dimensions, (0, 0, 0, 0))
            if self.image is None
            else self.image
        )
        mask = (
            (
                Image.new("RGBA", dimensions, (0, 0, 0, 0))
                if self.mask is None
                else self.mask
            )
            if with_mask
            else None
        )
        color_scheme = self.color_scheme or throw(RuntimeError("Missing color schema."))
        polarity = self.polarity or throw(RuntimeError("Missing polarity."))
        # Unset command buffer to prevent unintended reuse.
        self.command_buffer = None
        self.polarity = None

        return RasterRenderingFrame(
            command_buffer=command_buffer,
            bounding_box=bbox,
            image=image,
            mask=mask,
            color_scheme=color_scheme,
            polarity=polarity,
            is_region=self.is_region,
        )


class RasterRenderingFrame:
    """Container for rendering variables."""

    def __init__(
        self,
        command_buffer: ReadonlyCommandBuffer2,
        bounding_box: BoundingBox,
        image: Image.Image,
        mask: Optional[Image.Image],
        color_scheme: ColorScheme,
        polarity: Polarity,
        *,
        is_region: bool = False,
    ) -> None:
        self.command_buffer = command_buffer
        self.bounding_box = bounding_box
        self.image = image
        self.layer = ImageDraw.ImageDraw(image)
        self.mask = mask
        self.mask_draw = None if mask is None else ImageDraw.ImageDraw(mask)
        self.color_scheme = color_scheme
        self.polarity = polarity
        self.is_region = is_region

    def get_aperture(self) -> RasterAperture:
        """Return aperture."""
        if self.mask is None:
            msg = "Invalid aperture mask."
            raise RuntimeError(msg)
        return RasterAperture(image=self.image, mask=self.mask)

    def get_color(self, polarity: Polarity) -> str:
        """Get color for specified polarity."""
        if self.polarity == Polarity.Dark:
            return self._get_color(polarity)
        return self._get_color(polarity.invert())

    def _get_color(self, polarity: Polarity) -> str:
        if self.is_region:
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
        return "#00000000"

    def line(self, polarity: Polarity, *args: Any, **kwargs: Any) -> None:
        """Draw line on image."""
        kwargs["fill"] = self.get_color(polarity)
        self.layer.line(*args, **kwargs)
        if self.mask_draw is not None:
            kwargs["fill"] = self.get_mask_color(polarity)
            self.mask_draw.line(*args, **kwargs)

    def arc(self, polarity: Polarity, *args: Any, **kwargs: Any) -> None:
        """Draw arc on image."""
        kwargs["fill"] = self.get_color(polarity)
        self.layer.arc(*args, **kwargs)
        if self.mask_draw is not None:
            kwargs["fill"] = self.get_mask_color(polarity)
            self.mask_draw.arc(*args, **kwargs)

    def ellipse(self, polarity: Polarity, *args: Any, **kwargs: Any) -> None:
        """Draw ellipse on image."""
        kwargs["fill"] = self.get_color(polarity)
        self.layer.ellipse(*args, **kwargs)
        if self.mask_draw is not None:
            kwargs["fill"] = self.get_mask_color(polarity)
            self.mask_draw.ellipse(*args, **kwargs)

    def rectangle(self, polarity: Polarity, *args: Any, **kwargs: Any) -> None:
        """Draw rectangle on image."""
        kwargs["fill"] = self.get_color(polarity)
        self.layer.rectangle(*args, **kwargs)
        if self.mask_draw is not None:
            kwargs["fill"] = self.get_mask_color(polarity)
            self.mask_draw.rectangle(*args, **kwargs)

    def rounded_rectangle(self, polarity: Polarity, *args: Any, **kwargs: Any) -> None:
        """Draw rounded rectangle on image."""
        kwargs["fill"] = self.get_color(polarity)
        self.layer.rounded_rectangle(*args, **kwargs)
        if self.mask_draw is not None:
            kwargs["fill"] = self.get_mask_color(polarity)
            self.mask_draw.rounded_rectangle(*args, **kwargs)

    def regular_polygon(self, polarity: Polarity, *args: Any, **kwargs: Any) -> None:
        """Draw regular polygon on image."""
        kwargs["fill"] = self.get_color(polarity)
        self.layer.regular_polygon(*args, **kwargs)
        if self.mask_draw is not None:
            kwargs["fill"] = self.get_mask_color(polarity)
            self.mask_draw.regular_polygon(*args, **kwargs)

    def polygon(self, polarity: Polarity, *args: Any, **kwargs: Any) -> None:
        """Draw polygon on image."""
        kwargs["fill"] = self.get_color(polarity)
        self.layer.polygon(*args, **kwargs)
        if self.mask_draw is not None:
            kwargs["fill"] = self.get_mask_color(polarity)
            self.mask_draw.polygon(*args, **kwargs)

    def paste(self, *args: Any, **kwargs: Any) -> None:
        """Draw polygon on image."""
        self.image.paste(*args, **kwargs)
        if self.mask is not None:
            self.mask.paste(*args, **kwargs)

    def region_mode(self) -> ContextManager[None]:
        """Set rendering mode to region."""

        @contextmanager
        def _with() -> Generator[None, None, None]:
            self.is_region = True
            yield
            self.is_region = False

        return _with()


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
        self.frame_builder = (
            RasterRenderingFrameBuilder()
            .set_dpmm(self.dpmm)
            .set_scale(self.scale)
            .set_color_scheme(self.color_scheme)
        )

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
            self.frame_builder.set_polarity(Polarity.Dark)
            .set_command_buffer(command_buffer)
            .build(with_mask=False),
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

    def convert_xy(self, v: Vector2D) -> tuple[int, int]:
        """Convert vector coordinates to coordinates in image space."""
        return (
            self.convert_x(v.x),
            self.convert_y(v.y),
        )

    def convert_x(self, x: Offset) -> int:
        """Convert y offset to y coordinate in image space."""
        origin_offset_x = self.frame.bounding_box.min_x.as_millimeters()
        corrected_position_x = x.as_millimeters() - origin_offset_x
        return custom_round(
            corrected_position_x * self.scale * self.dpmm - Decimal(0.5),
        )

    def convert_y(self, y: Offset) -> int:
        """Convert y offset to y coordinate in image space."""
        origin_offset_y = self.frame.bounding_box.min_y.as_millimeters()
        corrected_position_y = y.as_millimeters() - origin_offset_y
        return custom_round(
            corrected_position_y * self.scale * self.dpmm - Decimal(0.5),
        )

    def convert_size(self, diameter: Offset) -> int:
        """Convert y offset to pixel y coordinate."""
        return max(custom_round(diameter.as_millimeters() * self.scale * self.dpmm), 1)

    def convert_bbox(self, bbox: BoundingBox) -> tuple[int, int, int, int]:
        """Convert bounding box region to pixel coordinates bbox."""
        return (
            self.convert_x(bbox.min_x),
            self.convert_y(bbox.min_y),
            self.convert_x(bbox.max_x),
            self.convert_y(bbox.max_y),
        )

    def get_aperture(self, aperture_id: str) -> Optional[RasterAperture]:
        """Get SVG group representing aperture."""
        return self.apertures.get(aperture_id)

    def set_aperture(
        self,
        aperture_id: str,
        raster_aperture: RasterAperture,
    ) -> None:
        """Set SVG group representing aperture."""
        self.apertures[aperture_id] = raster_aperture

    def get_aperture_id(self, aperture: Aperture2, transform: ApertureTransform) -> str:
        """Return combined ID for listed aperture."""
        return (
            f"{aperture.identifier}%{transform.polarity.value}"
            f"%{transform.get_transform_key()}"
        )

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

        self.frame.line(
            command.transform.polarity,
            (
                self.convert_x(command.start_point.x),
                self.convert_y(command.start_point.y),
                self.convert_x(command.end_point.x),
                self.convert_y(command.end_point.y),
            ),
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

        if end_angle < start_angle:
            end_angle += 360

        if end_angle == start_angle:
            start_angle = 360
            end_angle = 0

        self.frame.arc(
            command.transform.polarity,
            bbox,
            end_angle,
            start_angle,
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

        self.frame.arc(
            command.transform.polarity,
            bbox,
            start_angle,
            end_angle,
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

    def render_flash_circle(self, command: Flash2, aperture: Circle2) -> None:
        """Render flash circle to target image."""
        aperture_id = self.get_aperture_id(aperture, command.transform)
        raster_aperture = self.get_aperture(aperture_id)

        if raster_aperture is None:
            bbox = list(self.convert_bbox(command.get_bounding_box()))
            # Circles which are drawn with small amount of pixels are offset by 1 pixel
            # for some reason. This is a first part of workaround for that. 30 pixels is
            # an empirically determined threshold after which the offset is not needed
            # anymore. We need to increase size of the bounding box by 1 pixel to
            # fit a circle which size will also be increased by 1 pixel.
            if abs(bbox[0] - bbox[2]) <= 35:  # noqa: PLR2004
                self.frame_builder.set_pixel_dimension_offsets(x=1, y=1)

            # Unfortunately workaround implemented just above forces frame generation
            # to be deferred to here.
            frame_builder = self.frame_builder.set_polarity(
                command.transform.polarity
            ).set_command_buffer_from_list([command])
            self.push_render_frame(frame_builder.build())
            # Additionally we have to clean up frame_builder state we have altered.
            self.frame_builder.set_pixel_dimension_offsets()

            # We have to recalculate a bounding box after jumping into new frame as
            # dimensions of the frame likely changed, therefore relative position of
            # bounding box also changed.
            bbox = list(self.convert_bbox(command.get_bounding_box()))
            # This is a second part of workaround for circles which are drawn with small
            # amount of pixels. We need to increase size of the circle itself. We
            # couldn't do it earlier because we need to recalculate bbox for new frame.
            if abs(bbox[0] - bbox[2]) <= 35:  # noqa: PLR2004
                bbox[2] += 1

            self.frame.ellipse(
                Polarity.Dark,
                bbox,
            )
            self._make_hole(command, aperture)

            frame = self.pop_render_frame()
            raster_aperture = frame.get_aperture()
            self.set_aperture(aperture_id, raster_aperture)

        self._paste_aperture(command, raster_aperture)

    def _make_hole(
        self,
        command: Flash2,
        aperture: Circle2 | Rectangle2 | Obround2 | Polygon2,
    ) -> None:
        if aperture.hole_diameter is None:
            return
        self.frame.ellipse(
            Polarity.Clear,
            self.convert_bbox(
                BoundingBox(
                    min_x=-(aperture.hole_diameter / 2),
                    min_y=-(aperture.hole_diameter / 2),
                    max_x=aperture.hole_diameter / 2,
                    max_y=aperture.hole_diameter / 2,
                )
                + command.flash_point,
            ),
        )

    def _paste_aperture(self, command: Flash2, aperture_image: RasterAperture) -> None:
        bbox = command.get_bounding_box()
        origin_x, origin_y = self.convert_bbox(bbox)[0:2]
        self.frame.paste(
            aperture_image.image,
            (origin_x, origin_y),
            mask=aperture_image.mask,
        )

    def render_flash_no_circle(self, command: Flash2, aperture: NoCircle2) -> None:
        """Render flash no circle aperture to target image."""

    def render_flash_rectangle(self, command: Flash2, aperture: Rectangle2) -> None:
        """Render flash rectangle to target image."""
        aperture_id = self.get_aperture_id(aperture, command.transform)
        raster_aperture = self.get_aperture(aperture_id)

        if raster_aperture is None:
            self.push_render_frame(
                self.frame_builder.set_polarity(command.transform.polarity)
                .set_command_buffer_from_list([command])
                .build(),
            )
            edge_offset_vector = Vector2D(
                x=aperture.x_size / 2,
                y=Offset.new(0),
            ).get_rotated(aperture.rotation)

            max_xy = command.flash_point + edge_offset_vector
            min_xy = command.flash_point - edge_offset_vector

            start_xy = min_xy
            end_xy = max_xy

            tangent_vector = Vector2D(
                x=Offset.new(0),
                y=aperture.y_size / 2,
            ).get_rotated(aperture.rotation)

            self.frame.polygon(
                Polarity.Dark,
                (
                    (self.convert_xy(start_xy + tangent_vector)),
                    (self.convert_xy(start_xy - tangent_vector)),
                    (self.convert_xy(end_xy - tangent_vector)),
                    (self.convert_xy(end_xy + tangent_vector)),
                ),
            )
            self._make_hole(command, aperture)

            frame = self.pop_render_frame()
            raster_aperture = frame.get_aperture()
            self.set_aperture(aperture_id, raster_aperture)

        self._paste_aperture(command, raster_aperture)

    def render_flash_obround(self, command: Flash2, aperture: Obround2) -> None:
        """Render flash obround to target image."""
        aperture_id = self.get_aperture_id(aperture, command.transform)
        aperture_image = self.get_aperture(aperture_id)

        if aperture_image is None:
            self.push_render_frame(
                self.frame_builder.set_polarity(command.transform.polarity)
                .set_command_buffer_from_list([command])
                .build(),
            )

            self.frame.rounded_rectangle(
                Polarity.Dark,
                self.convert_bbox(
                    BoundingBox.from_rectangle(aperture.x_size, aperture.y_size)
                    + command.flash_point,
                ),
                radius=min(
                    self.convert_size(aperture.x_size),
                    self.convert_size(aperture.y_size),
                )
                / 2,
            )
            self._make_hole(command, aperture)

            frame = self.pop_render_frame()
            aperture_image = frame.get_aperture()
            self.set_aperture(aperture_id, aperture_image)

        self._paste_aperture(command, aperture_image)

    def render_flash_polygon(self, command: Flash2, aperture: Polygon2) -> None:
        """Render flash polygon to target image."""
        aperture_id = self.get_aperture_id(aperture, command.transform)
        aperture_image = self.get_aperture(aperture_id)

        if aperture_image is None:
            self.push_render_frame(
                self.frame_builder.set_polarity(command.transform.polarity)
                .set_command_buffer_from_list([command])
                .build(),
            )

            outer_diameter = aperture.outer_diameter
            radius = self.convert_size(outer_diameter / 2)
            # In PIL rotation angle goes in opposite direction than in Gerber and
            # starts from different orientation.
            rotation = -float(aperture.rotation) - 90.0
            bbox = command.get_bounding_box()

            self.frame.regular_polygon(
                Polarity.Dark,
                (
                    self.convert_x(bbox.min_x) + radius,
                    self.convert_y(bbox.min_y) + radius,
                    radius,
                ),
                n_sides=aperture.number_vertices,
                rotation=rotation,
            )
            self._make_hole(command, aperture)

            frame = self.pop_render_frame()
            aperture_image = frame.get_aperture()
            self.set_aperture(aperture_id, aperture_image)

        self._paste_aperture(command, aperture_image)

    def render_flash_macro(self, command: Flash2, aperture: Macro2) -> None:
        """Render flash macro aperture to target image."""
        aperture_id = self.get_aperture_id(aperture, command.transform)
        aperture_image = self.get_aperture(aperture_id)

        if aperture_image is None:
            self.push_render_frame(
                self.frame_builder.set_polarity(command.transform.polarity)
                .set_command_buffer(aperture.command_buffer)
                .build(),
            )

            for cmd in aperture.command_buffer:
                cmd.render(self.renderer)

            frame = self.pop_render_frame()
            aperture_image = frame.get_aperture()
            self.set_aperture(aperture_id, aperture_image)

        self._paste_aperture(command, aperture_image)

    def render_region(self, command: Region2) -> None:
        """Render region to target image."""
        if len(command.command_buffer) == 0:
            return

        with self.frame.region_mode():
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

            self.frame.polygon(command.transform.polarity, points)

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
        point_count = self.convert_size(arc_length / 1.618)
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
        point_count = self.convert_size(arc_length / 2)
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
        self.apertures.clear()
        gc.collect(0)
        gc.collect(1)
        gc.collect(2)
        self.frame.image = self.frame.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        gc.collect(0)
        gc.collect(1)
        gc.collect(2)

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
            if self.image.mode.casefold() != options.pixel_format.value.casefold():
                image = self.image.convert(options.pixel_format.value)
            else:
                image = self.image

            kwargs = {}

            if options.image_format != ImageFormat.AUTO:
                kwargs["format"] = options.image_format.value

            if options.quality is not None:
                kwargs["quality"] = options.quality

            image.save(output, **kwargs)
            return

        self.image.save(output)

    def get_image(self) -> Image.Image:
        """Get image reference."""
        return self.image


class ImageFormat(Enum):
    """List of officially supported raster image formats."""

    PNG = "png"
    JPEG = "jpg"
    AUTO = "auto"


class PixelFormat(Enum):
    """List of officially supported pixel formats."""

    RGB = "RGB"
    RGBA = "RGBA"


class RasterFormatOptions(FormatOptions):
    """Raster Format specific options."""

    def __init__(
        self,
        image_format: ImageFormat = ImageFormat.AUTO,
        pixel_format: PixelFormat = PixelFormat.RGBA,
        quality: int = 85,
    ) -> None:
        self.image_format = image_format
        self.pixel_format = pixel_format
        self.quality = quality
