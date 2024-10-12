"""Errors which may be called by API layer."""

from __future__ import annotations


class GerberX3APIError(Exception):
    """Base class for API errors.

    Exceptions derived from this exception are exclusively raised in PyGerber's Gerber
    X3 high level API. This exception can be used in
    `#!python try: ... except GerberX3APIError: ...` block to catch all exceptions
    raised by this API while allowing other exceptions to interrupt execution.
    """


class PathToGerberJobProjectNotDefinedError(GerberX3APIError):
    """Raised when path to Gerber Job project is not defined."""
