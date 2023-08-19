"""Drawing backends for Gerber files rendering."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from pygerber.backend.abstract.errors import BackendNotSupportedError
from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend


class BackendName(Enum):
    """Available rendering modes."""

    Rasterized2D = "rasterized_2d"
    Vector2D = "vector_2d"
    Model3D = "model_3d"

    @staticmethod
    def get_backend_class(backend: str | BackendName) -> type[Backend]:
        """Return backend class."""
        if str(backend) == BackendName.Rasterized2D.value:
            return Rasterized2DBackend

        raise BackendNotSupportedError(str(backend))

    def __str__(self) -> str:
        return self.value
