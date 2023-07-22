"""Module contains classes-handles to drawing apertures."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID

if TYPE_CHECKING:
    from pygerber.backend.abstract.aperture_draws.aperture_draw import ApertureDraw


class PrivateApertureHandle:
    """Base class for creating Gerber X3 apertures."""

    _bbox: Optional[BoundingBox] = None

    def __init__(
        self,
        aperture_id: ApertureID,
        private_id: int,
        backend: Backend,
    ) -> None:
        """Initialize aperture handle."""
        self.aperture_id = aperture_id
        self.private_id = private_id
        self.backend = backend
        self.aperture_draws: list[ApertureDraw] = []

    def add_draw(self, draw: ApertureDraw) -> None:
        """Add circle to aperture."""
        self.aperture_draws.append(draw)

    @abstractmethod
    def finalize_aperture_creation(self) -> None:
        """Draw aperture and store result."""

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        if self._bbox is None:
            bbox = BoundingBox.NULL

            for aperture_draw in self.aperture_draws:
                bbox += aperture_draw.get_bounding_box()

            self._bbox = bbox

        return self._bbox

    def get_public_handle(self) -> PublicApertureHandle:
        """Return immutable aperture handle."""
        return PublicApertureHandle(
            aperture_id=self.aperture_id,
            private_id=self.private_id,
        )


class PublicApertureHandle(BaseModel):
    """Immutable handle to drawing aperture."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    aperture_id: ApertureID
    private_id: int