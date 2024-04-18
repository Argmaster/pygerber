"""Base error classes used in this module."""

from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.bases.token import Token


class ParserError(ValueError):
    """Base class for parser errors.

    Exceptions derived from this exception are exclusively raised in PyGerber's Gerber
    X3 Parser. This exception can be used in
    `#!python try: ... except ParserError: ...` block to catch all exceptions
    raised by Parser while allowing other exceptions to interrupt execution.
    """

    def get_message(self) -> str:
        """Get parser error help message."""
        return f"{self.__class__.__qualname__}: {self.__doc__}"


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

    def __init__(self, token: Token, *args: object) -> None:
        super().__init__(*args)
        self.token = token

    def __str__(self) -> str:
        return f"{self.token} {self.token.get_token_position()}"


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
