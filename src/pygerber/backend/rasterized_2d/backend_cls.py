"""Backend for rasterized rendering of Gerber files."""
from __future__ import annotations

from pygerber.backend.abstract.backend_cls import Backend


class Rasterized2DBackend(Backend):
    """Drawing backend interface."""
