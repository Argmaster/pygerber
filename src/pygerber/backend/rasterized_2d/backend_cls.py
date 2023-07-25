"""Backend for rasterized rendering of Gerber files."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from PIL import Image, ImageDraw

from pygerber.backend.abstract.backend_cls import Backend, BackendOptions
from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.backend.rasterized_2d.aperture_draws.aperture_draw_circle import (
    Rasterized2DApertureDrawCircle,
)
from pygerber.backend.rasterized_2d.aperture_draws.aperture_draw_polygon import (
    Rasterized2DApertureDrawPolygon,
)
from pygerber.backend.rasterized_2d.aperture_draws.aperture_draw_rectangle import (
    Rasterized2DApertureDrawRectangle,
)
from pygerber.backend.rasterized_2d.aperture_handle import (
    Rasterized2DPrivateApertureHandle,
)
from pygerber.backend.rasterized_2d.draw_actions.draw_action_mixin import (
    Rasterized2DDrawActionMixin,
)
from pygerber.backend.rasterized_2d.draw_actions.draw_arc import Rasterized2DDrawArc
from pygerber.backend.rasterized_2d.draw_actions.draw_flash import Rasterized2DDrawFlash
from pygerber.backend.rasterized_2d.draw_actions.draw_line import Rasterized2DDrawLine
from pygerber.backend.rasterized_2d.draw_actions_handle import (
    Rasterized2DDrawActionsHandle,
)
from pygerber.backend.rasterized_2d.errors import ApertureImageNotInitializedError
from pygerber.backend.rasterized_2d.result_handle import Rasterized2DResultHandle
from pygerber.gerberx3.state_enums import Polarity

if TYPE_CHECKING:
    from pathlib import Path

    from pygerber.backend.abstract.aperture_draws.aperture_draw_circle import (
        ApertureDrawCircle,
    )
    from pygerber.backend.abstract.aperture_draws.aperture_draw_polygon import (
        ApertureDrawPolygon,
    )
    from pygerber.backend.abstract.aperture_draws.aperture_draw_rectangle import (
        ApertureDrawRectangle,
    )
    from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
    from pygerber.backend.abstract.draw_actions.draw_action import DrawAction
    from pygerber.backend.abstract.draw_actions.draw_arc import DrawArc
    from pygerber.backend.abstract.draw_actions.draw_flash import DrawFlash
    from pygerber.backend.abstract.draw_actions.draw_line import DrawLine
    from pygerber.backend.abstract.draw_actions_handle import DrawActionsHandle
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

    def draw(self, draw_actions: List[DrawAction]) -> ResultHandle:
        """Execute all draw actions to create visualization."""
        raw_bbox = self._get_draw_actions_bounding_box(draw_actions)

        if self.options.include_debug_padding:
            bbox = raw_bbox.scale(Decimal(2))
        else:
            bbox = raw_bbox

        size = bbox.get_size()
        self.image_coordinates_correction = bbox.get_min_vector()

        image_size = size.as_pixels(self.dpi)
        # Image must be at least 1x1, otherwise Pillow crashes while saving.
        x, y = image_size
        image_size = (max(x, 0) + 1, max(y, 0) + 1)

        self.image = Image.new(mode="L", size=image_size, color=0)

        result_handle = super().draw(draw_actions)
        Rasterized2DDrawActionMixin.draw_bounding_box(
            raw_bbox,
            self,
            Polarity.DEBUG,
            2,  #  Just slightly bigger than bounding boxes of flashes etc.
        )
        return result_handle

    def _get_draw_actions_bounding_box(
        self,
        draw_actions: List[DrawAction],
    ) -> BoundingBox:
        bbox = BoundingBox.NULL

        for draw_action in draw_actions:
            bbox += draw_action.get_bounding_box()

        return bbox

    @property
    def image(self) -> Image.Image:
        """Aperture image."""
        if self._image is None:
            raise ApertureImageNotInitializedError
        return self._image

    @image.setter
    def image(self, value: Image.Image) -> None:
        """Aperture image."""
        self._image = value

    @property
    def image_draw(self) -> ImageDraw.ImageDraw:
        """Acquire drawing interface."""
        return ImageDraw.Draw(self.image)

    def get_result_handle(self) -> ResultHandle:
        """Return result handle to visualization."""
        return Rasterized2DResultHandle(self.image)

    def get_aperture_handle_cls(self) -> type[PrivateApertureHandle]:
        """Get backend-specific implementation of aperture handle class."""
        return Rasterized2DPrivateApertureHandle

    def get_aperture_draw_circle_cls(self) -> type[ApertureDrawCircle]:
        """Get backend-specific implementation of aperture circle component class."""
        return Rasterized2DApertureDrawCircle

    def get_aperture_draw_rectangle_cls(self) -> type[ApertureDrawRectangle]:
        """Get backend-specific implementation of aperture rectangle component class."""
        return Rasterized2DApertureDrawRectangle

    def get_aperture_draw_polygon_cls(self) -> type[ApertureDrawPolygon]:
        """Get backend-specific implementation of aperture polygon component class."""
        return Rasterized2DApertureDrawPolygon

    def get_draw_actions_handle_cls(self) -> type[DrawActionsHandle]:
        """Return backend-specific implementation of draw actions handle."""
        return Rasterized2DDrawActionsHandle

    def get_draw_action_flash_cls(self) -> type[DrawFlash]:
        """Return backend-specific implementation of draw action flash."""
        return Rasterized2DDrawFlash

    def get_draw_action_line_cls(self) -> type[DrawLine]:
        """Return backend-specific implementation of draw action line."""
        return Rasterized2DDrawLine

    def get_draw_action_arc_cls(self) -> type[DrawArc]:
        """Return backend-specific implementation of draw action arc."""
        return Rasterized2DDrawArc
