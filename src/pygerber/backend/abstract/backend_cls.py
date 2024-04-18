"""Class interface for visualizing gerber files."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar, List, Optional, Type

from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.vector_2d import Vector2D

if TYPE_CHECKING:
    from pathlib import Path

    from pygerber.backend.abstract.aperture_handle import (
        PrivateApertureHandle,
        PublicApertureHandle,
    )
    from pygerber.backend.abstract.draw_commands.draw_arc import DrawArc
    from pygerber.backend.abstract.draw_commands.draw_circle import (
        DrawCircle,
    )
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.backend.abstract.draw_commands.draw_paste import DrawPaste
    from pygerber.backend.abstract.draw_commands.draw_polygon import (
        DrawPolygon,
    )
    from pygerber.backend.abstract.draw_commands.draw_rectangle import (
        DrawRectangle,
    )
    from pygerber.backend.abstract.draw_commands.draw_region import DrawRegion
    from pygerber.backend.abstract.draw_commands.draw_vector_line import DrawVectorLine
    from pygerber.backend.abstract.draw_commands_handle import DrawCommandsHandle
    from pygerber.backend.abstract.drawing_target import DrawingTarget
    from pygerber.backend.abstract.result_handle import ResultHandle
    from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID


class BackendOptions:
    """Additional configuration which can be passed to backend."""

    def __init__(
        self,
        dump_apertures: Optional[Path] = None,
        *,
        draw_region_outlines: bool = False,
    ) -> None:
        """Initialize options."""
        self.dump_apertures = dump_apertures
        self.draw_region_outlines = draw_region_outlines


class Backend(ABC):
    """Drawing backend interface."""

    handles: list[PrivateApertureHandle]
    drawing_target: DrawingTarget
    bounding_box: BoundingBox
    coordinate_origin: Vector2D

    options_class: ClassVar[type[BackendOptions]] = BackendOptions

    def __init__(self, options: Optional[BackendOptions] = None) -> None:
        """Initialize backend."""
        self.options = self.options_class() if options is None else options
        self.handles = []

    def create_aperture_handle(self, aperture_id: ApertureID) -> PrivateApertureHandle:
        """Create new aperture handle."""
        handle = self.get_aperture_handle_cls()(
            aperture_id=aperture_id,
            private_id=len(self.handles),
            backend=self,
        )
        self.handles.append(handle)
        return handle

    def get_private_aperture_handle(
        self,
        public_aperture_handle: PublicApertureHandle,
    ) -> PrivateApertureHandle:
        """Get private aperture handle."""
        return self.handles[public_aperture_handle.private_id]

    def draw(self, draws: List[DrawCommand]) -> ResultHandle:
        """Execute all draw actions to create visualization."""
        self.draws = draws

        self.finalize_aperture_creation()
        self.bounding_box = self._get_draws_bounding_box(draws)
        self.coordinate_origin = self._get_coordinate_origin()
        self.drawing_target = self._create_drawing_target()
        self._pre_drawing_hook()

        with self.drawing_target:
            for draw_action in draws:
                draw_action.draw(self.drawing_target)

        self._post_drawing_hook()

        return self.get_result_handle()

    def finalize_aperture_creation(self) -> None:
        """Apply draw operations to aperture handles."""
        for handle in self.handles:
            handle.finalize_aperture_creation()

    def _get_draws_bounding_box(self, draws: List[DrawCommand]) -> BoundingBox:
        bbox: Optional[BoundingBox] = None

        for draw in draws:
            if bbox is not None:
                bbox += draw.get_bounding_box()
            else:
                bbox = draw.get_bounding_box()

        if bbox is not None:
            return bbox

        return BoundingBox.NULL

    def _get_coordinate_origin(self) -> Vector2D:
        return self.bounding_box.get_min_vector()

    @abstractmethod
    def _create_drawing_target(self) -> DrawingTarget:
        """Create drawing target object."""

    def _pre_drawing_hook(self) -> None:  # noqa: B027
        """Perform custom actions before drawing."""

    def _post_drawing_hook(self) -> None:  # noqa: B027
        """Perform custom actions after drawing."""

    @abstractmethod
    def get_result_handle(self) -> ResultHandle:
        """Return result handle to visualization."""

    @abstractmethod
    def get_aperture_handle_cls(self) -> Type[PrivateApertureHandle]:
        """Get backend-specific implementation of aperture handle class."""

    @abstractmethod
    def get_draw_circle_cls(self) -> Type[DrawCircle]:
        """Get backend-specific implementation of aperture circle component class."""

    @abstractmethod
    def get_draw_rectangle_cls(self) -> Type[DrawRectangle]:
        """Get backend-specific implementation of aperture rectangle component class."""

    @abstractmethod
    def get_draw_polygon_cls(self) -> Type[DrawPolygon]:
        """Get backend-specific implementation of aperture polygon component class."""

    @abstractmethod
    def get_draw_commands_handle_cls(self) -> type[DrawCommandsHandle]:
        """Return backend-specific implementation of draw actions handle."""

    @abstractmethod
    def get_draw_paste_cls(self) -> type[DrawPaste]:
        """Return backend-specific implementation of draw paste."""

    @abstractmethod
    def get_draw_region_cls(self) -> type[DrawRegion]:
        """Return backend-specific implementation of draw action region."""

    @abstractmethod
    def get_draw_vector_line_cls(self) -> type[DrawVectorLine]:
        """Return backend-specific implementation of draw action line."""

    @abstractmethod
    def get_draw_arc_cls(self) -> type[DrawArc]:
        """Return backend-specific implementation of draw action arc."""
