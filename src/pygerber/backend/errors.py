"""Backend related errors."""
from __future__ import annotations


class BackendError(Exception):
    """Base class used by all backend errors."""


class BackendNotSupportedError(BackendError):
    """Raised when requesting backend which is not officially supported."""
