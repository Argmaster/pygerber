"""Errors which may be called by API layer."""

from __future__ import annotations


class GerberX3APIError(Exception):
    """Base class for API errors.

    Exceptions derived from this exception are exclusively raised in PyGerber's Gerber
    X3 high level API. This exception can be used in
    `#!python try: ... except GerberX3APIError: ...` block to catch all exceptions
    raised by this API while allowing other exceptions to interrupt execution.
    """


class RenderingResultNotReadyError(GerberX3APIError):
    """Raised when RenderingResult is requested before it was rendered.

    `Layer.get_rendering_result()` method can only be called after `Layer.render()`.
    Breaking this rule will cause this exception to be raised.
    """


class MutuallyExclusiveViolationError(GerberX3APIError):
    """Raised when two or more of mutually exclusive parameters are provided.

    `LayerParams` class accepts three mutually exclusive fields, `source_path`,
    `source_code` and `source_buffer` for providing source code to `Layer`.
    When more than one of those options is set, this exception will be raised.
    """
