"""Backend for rasterized rendering of Gerber files."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, ClassVar, Optional

from PIL import Image

from pygerber.backend.abstract.backend_cls import Backend, BackendOptions
from pygerber.backend.abstract.offset import Offset
from pygerber.backend.rasterized_2d.aperture_handle import (
    Rasterized2DPrivateApertureHandle,
)
from pygerber.backend.rasterized_2d.draw_commands.draw_arc import Rasterized2DDrawArc
from pygerber.backend.rasterized_2d.draw_commands.draw_bounding_box import (
    Rasterized2DApertureDrawBoundingBox,
)
from pygerber.backend.rasterized_2d.draw_commands.draw_circle import (
    Rasterized2DApertureDrawCircle,
)
from pygerber.backend.rasterized_2d.draw_commands.draw_paste import (
    Rasterized2DDrawPaste,
)
from pygerber.backend.rasterized_2d.draw_commands.draw_polygon import (
    Rasterized2DApertureDrawPolygon,
)
from pygerber.backend.rasterized_2d.draw_commands.draw_rectangle import (
    Rasterized2DApertureDrawRectangle,
)
from pygerber.backend.rasterized_2d.draw_commands.draw_vector_line import (
    Rasterized2DDrawVectorLine,
)
from pygerber.backend.rasterized_2d.draw_commands_handle import (
    Rasterized2DDrawActionsHandle,
)
from pygerber.backend.rasterized_2d.drawing_target import Rasterized2DDrawingTarget
from pygerber.backend.rasterized_2d.result_handle import Rasterized2DResultHandle
from pygerber.gerberx3.state_enums import Polarity

if TYPE_CHECKING:
    from pathlib import Path

    from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
    from pygerber.backend.abstract.draw_commands.draw_arc import DrawArc
    from pygerber.backend.abstract.draw_commands.draw_circle import (
        DrawCircle,
    )
    from pygerber.backend.abstract.draw_commands.draw_paste import DrawPaste
    from pygerber.backend.abstract.draw_commands.draw_polygon import (
        DrawPolygon,
    )
    from pygerber.backend.abstract.draw_commands.draw_rectangle import (
        DrawRectangle,
    )
    from pygerber.backend.abstract.draw_commands.draw_vector_line import DrawVectorLine
    from pygerber.backend.abstract.draw_commands_handle import DrawCommandsHandle
    from pygerber.backend.abstract.drawing_target import DrawingTarget
    from pygerber.backend.abstract.result_handle import ResultHandle


class Rasterized2DBackendOptions(BackendOptions):
    """Additional configuration which can be passed to backend."""

    def __init__(
        self,
        dpi: int = 300,
        dump_apertures: Optional[Path] = None,
        *,
        include_debug_padding: bool = False,
        include_bounding_boxes: bool = False,
    ) -> None:
        """Initialize options."""
        self.dpi = dpi
        self.include_debug_padding = include_debug_padding
        self.include_bounding_boxes = include_bounding_boxes
        super().__init__(dump_apertures=dump_apertures)


class Rasterized2DBackend(Backend):
    """Drawing backend interface."""

    options: Rasterized2DBackendOptions
    drawing_target: Rasterized2DDrawingTarget

    options_class: ClassVar[type[BackendOptions]] = Rasterized2DBackendOptions

    def __init__(self, options: Rasterized2DBackendOptions | None = None) -> None:
        """Initialize backend."""
        if options is not None and not isinstance(options, Rasterized2DBackendOptions):
            msg = (  # type: ignore[unreachable]
                "Expected Rasterized2DBackendOptions or None as options, got "
                + str(type(options))
            )
            raise TypeError(msg)
        super().__init__(options)

    @property
    def dpi(self) -> int:
        """Return image DPI."""
        return self.options.dpi

    def _create_drawing_target(self) -> DrawingTarget:
        """Execute all draw actions to create visualization."""
        raw_bbox = self.bounding_box

        if self.options.include_debug_padding:
            bbox = raw_bbox.scale(Decimal(2))
        else:
            bbox = raw_bbox

        size = bbox.get_size()
        coordinate_origin = bbox.get_min_vector()

        image_size = size.as_pixels(self.dpi)
        # Image must be at least 1x1, otherwise Pillow crashes while saving.
        x, y = image_size
        image_size = (max(x, 0) + 1, max(y, 0) + 1)

        return Rasterized2DDrawingTarget(
            coordinate_origin=coordinate_origin,
            bounding_box=bbox,
            target_image=Image.new(mode="L", size=image_size, color=0),
        )

    def _pre_drawing_hook(self) -> None:
        """Perform custom actions after drawing."""
        if self.options.include_bounding_boxes:
            self.draws.append(
                Rasterized2DApertureDrawBoundingBox(
                    backend=self,
                    polarity=Polarity.DEBUG,
                    bounding_box=self.bounding_box,
                    outline_padding=Offset.from_pixels(1, self.dpi),
                ),
            )

    def get_result_handle(self) -> ResultHandle:
        """Return result handle to visualization."""
        return Rasterized2DResultHandle(self.drawing_target.target_image)

    def get_aperture_handle_cls(self) -> type[PrivateApertureHandle]:
        """Get backend-specific implementation of aperture handle class."""
        return Rasterized2DPrivateApertureHandle

    def get_draw_circle_cls(self) -> type[DrawCircle]:
        """Get backend-specific implementation of aperture circle component class."""
        return Rasterized2DApertureDrawCircle

    def get_draw_rectangle_cls(self) -> type[DrawRectangle]:
        """Get backend-specific implementation of aperture rectangle component class."""
        return Rasterized2DApertureDrawRectangle

    def get_draw_polygon_cls(self) -> type[DrawPolygon]:
        """Get backend-specific implementation of aperture polygon component class."""
        return Rasterized2DApertureDrawPolygon

    def get_draw_commands_handle_cls(self) -> type[DrawCommandsHandle]:
        """Return backend-specific implementation of draw actions handle."""
        return Rasterized2DDrawActionsHandle

    def get_draw_paste_cls(self) -> type[DrawPaste]:
        """Return backend-specific implementation of draw action flash."""
        return Rasterized2DDrawPaste

    def get_draw_vector_line_cls(self) -> type[DrawVectorLine]:
        """Return backend-specific implementation of draw action line."""
        return Rasterized2DDrawVectorLine

    def get_draw_arc_cls(self) -> type[DrawArc]:
        """Return backend-specific implementation of draw action arc."""
        return Rasterized2DDrawArc
