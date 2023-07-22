"""Class interface for visualizing gerber files."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Optional, Type

from pygerber.backend.abstract.draw_actions.draw_action import DrawAction
from pygerber.backend.abstract.result_handle import ResultHandle

if TYPE_CHECKING:
    from pygerber.backend.abstract.aperture_draws.aperture_draw_circle import (
        ApertureDrawCircle,
    )
    from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
    from pygerber.backend.abstract.draw_actions_handle import DrawActionsHandle
    from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID


class BackendOptions:
    """Additional configuration which can be passed to backend."""

    def __init__(self) -> None:
        """Initialize options."""


class Backend(ABC):
    """Drawing backend interface."""

    handles: list[PrivateApertureHandle]

    def __init__(self, options: Optional[BackendOptions] = None) -> None:
        """Initialize backend."""
        self.options = BackendOptions() if options is None else options
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

    def draw(self, draw_actions: List[DrawAction]) -> ResultHandle:
        """Execute all draw actions to create visualization."""
        self.finalize_aperture_creation()

        for draw_action in draw_actions:
            draw_action.draw()

        return self.get_result_handle()

    def finalize_aperture_creation(self) -> None:
        """Apply draw operations to aperture handles."""
        for handle in self.handles:
            handle.finalize_aperture_creation()

    @abstractmethod
    def get_result_handle(self) -> ResultHandle:
        """Return result handle to visualization."""

    @abstractmethod
    def get_aperture_handle_cls(self) -> Type[PrivateApertureHandle]:
        """Get backend-specific implementation of aperture handle class."""

    @abstractmethod
    def get_aperture_draw_circle_cls(self) -> Type[ApertureDrawCircle]:
        """Get backend-specific implementation of aperture circle component class."""

    @abstractmethod
    def get_draw_actions_handle_cls(self) -> type[DrawActionsHandle]:
        """Return backend-specific implementation of draw actions handle."""
