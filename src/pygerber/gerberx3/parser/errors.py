"""Base error classes used in this module."""


from __future__ import annotations


class ParserError(ValueError):
    """Base class for parser errors."""


class ZeroOmissionNotSupportedError(ParserError):
    """Raised when incremental coordinates are selected. (Spec. 8.2.1.2)."""


class IncrementalCoordinatesNotSupportedError(ParserError):
    """Raised when incremental coordinates are selected. (Spec. 8.2.1.2)."""


class UnsupportedCoordinateTypeError(ParserError):
    """Raised for unsupported coordinate types."""


class InvalidCoordinateLengthError(ParserError):
    """Raised when coordinate string is too long."""


class ParserFatalError(ParserError):
    """Raised when parser encounters fatal failure from non-parser specific
    exception.
    """


class OnUpdateDrawingStateError(ParserError):
    """Raised when parser encounters fatal failure from non-parser specific
    exception during call to .update_drawing_state() call.
    """


class UnitNotSetError(ParserError):
    """Raised when operation which requires units to be set is executed before units
    are set.
    """


class ApertureNotDefinedError(ParserError):
    """Raised when undefined aperture is selected."""


class CoordinateFormatNotSetError(ParserError):
    """Raised when coordinate parser is requested before coordinate format was set."""


class ApertureNotSelectedError(ParserError):
    """Raised when attempting to use aperture without selecting it first."""


class ExitParsingProcessInterrupt(Exception):  # noqa: N818
    """Raised to stop parsing."""
