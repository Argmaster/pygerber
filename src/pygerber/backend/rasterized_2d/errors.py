"""Base error classes used in this module."""

from __future__ import annotations

from pygerber.backend.abstract.errors import BackendError


class Rasterized2DBackendError(BackendError):
    """Base class for backend errors."""


class ApertureImageNotInitializedError(Rasterized2DBackendError):
    """Raised when aperture image is requested before it was initialized."""


class BackendImageNotInitializedError(Rasterized2DBackendError):
    """Raised when backend canvas image is requested before initialization."""
