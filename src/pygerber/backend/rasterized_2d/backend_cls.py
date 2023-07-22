"""Backend for rasterized rendering of Gerber files."""
from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.backend.abstract.backend_cls import Backend, BackendOptions
from pygerber.backend.rasterized_2d.aperture_draws.aperture_draw_circle import (
    Rasterized2DApertureDrawCircle,
)
from pygerber.backend.rasterized_2d.aperture_handle import (
    Rasterized2DPrivateApertureHandle,
)
from pygerber.backend.rasterized_2d.draw_actions_handle import (
    Rasterized2DDrawActionsHandle,
)
from pygerber.backend.rasterized_2d.result_handle import Rasterized2DResultHandle

if TYPE_CHECKING:
    from pygerber.backend.abstract.aperture_draws.aperture_draw_circle import (
        ApertureDrawCircle,
    )
    from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
    from pygerber.backend.abstract.draw_actions_handle import DrawActionsHandle
    from pygerber.backend.abstract.result_handle import ResultHandle


class Rasterized2DBackendOptions(BackendOptions):
    """Additional configuration which can be passed to backend."""

    def __init__(self, dpi: int = 300) -> None:
        """Initialize options."""
        self.dpi = dpi


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

    def get_result_handle(self) -> ResultHandle:
        """Return result handle to visualization."""
        return Rasterized2DResultHandle()

    def get_aperture_handle_cls(self) -> type[PrivateApertureHandle]:
        """Get backend-specific implementation of aperture handle class."""
        return Rasterized2DPrivateApertureHandle

    def get_aperture_draw_circle_cls(self) -> type[ApertureDrawCircle]:
        """Get backend-specific implementation of aperture circle component class."""
        return Rasterized2DApertureDrawCircle

    def get_draw_actions_handle_cls(self) -> type[DrawActionsHandle]:
        """Return backend-specific implementation of draw actions handle."""
        return Rasterized2DDrawActionsHandle
