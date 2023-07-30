"""Errors which may be called by API layer."""
from __future__ import annotations


class GerberX3APIError(Exception):
    """Base class for API errors."""


class RenderingResultNotReadyError(GerberX3APIError):
    """Raised when RenderingResult is requested before it was rendered."""


class MutuallyExclusiveViolationError(GerberX3APIError):
    """Raised when two or more of mutually exclusive parameters are provided."""
