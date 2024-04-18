"""Base error classes used in this module."""

from __future__ import annotations


class BackendError(ValueError):
    """Base class for backend errors."""


class BackendNotSupportedError(BackendError):
    """Raised when requesting backend which is not officially supported."""
