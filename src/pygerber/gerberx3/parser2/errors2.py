"""Base error classes used in this module."""

from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.bases.token import Token


class Parser2Error(ValueError):
    """Base class for parser errors.

    Exceptions derived from this exception are exclusively raised in PyGerber's Gerber
    X3 Parser. This exception can be used in
    `#!python try: ... except Parser2Error: ...` block to catch all exceptions
    raised by Parser while allowing other exceptions to interrupt execution.
    """

    def get_message(self) -> str:
        """Get parser error help message."""
        return f"{self.__class__.__qualname__}: {self.__doc__}"


class ZeroOmissionNotSupported2Error(Parser2Error):
    """Raised when incremental coordinates are selected. (Spec. 8.2.1.2)."""


class IncrementalCoordinatesNotSupported2Error(Parser2Error):
    """Raised when incremental coordinates are selected. (Spec. 8.2.1.2)."""


class UnsupportedCoordinateType2Error(Parser2Error):
    """Raised for unsupported coordinate types."""


class InvalidCoordinateLength2Error(Parser2Error):
    """Raised when coordinate string is too long."""


class ParserFatal2Error(Parser2Error):
    """Raised when parser encounters fatal failure from non-parser specific
    exception.
    """


class OnUpdateDrawingState2Error(Parser2Error):
    """Raised when parser encounters fatal failure from non-parser specific
    exception during call to .update_drawing_state() call.
    """

    def __init__(self, token: Token, *args: object) -> None:
        super().__init__(*args)
        self.token = token

    def __str__(self) -> str:
        return f"{self.token} {self.token.get_token_position()}"


class UnitNotSet2Error(Parser2Error):
    """Raised when operation which requires units to be set is executed before units
    are set.
    """


class ReferencedNotInitializedBlockBufferError(Parser2Error):
    """Raised when Gerber file references block buffer which has not been
    initialized, ie. when block aperture was not correctly started.
    """


class UnnamedBlockApertureNotAllowedError(Parser2Error):
    """Raised when aperture block with no ID is encountered."""


class RegionNotInitializedError(Parser2Error):
    """Raised when region is modified without being accessed without initialization."""


class ApertureNotDefined2Error(Parser2Error):
    """Raised when undefined aperture is selected."""


class MacroNotDefinedError(Parser2Error):
    """Raised when undefined macro is referenced."""


class NoValidArcCenterFoundError(Parser2Error):
    """Raised when no valid arc center point can not be deduced from IJ offset in
    single quadrant mode (G74).
    """


class CoordinateFormatNotSet2Error(Parser2Error):
    """Raised when coordinate parser is requested before coordinate format was set."""


class ApertureNotSelected2Error(Parser2Error):
    """Raised when attempting to use aperture without selecting it first."""


class StepAndRepeatNotInitializedError(Parser2Error):
    """Raised when step and repeat block is closed without being correctly opened."""


class MacroNotInitializedError(Parser2Error):
    """Raised when macro statement buffer is requested without being correctly
    initialized.
    """


class StandardAttributeError(Parser2Error):
    """Raised when parser encounters an error while processing a standard attribute."""


class MissingNameFieldError(StandardAttributeError):
    """Raised when a missing name field is detected."""


class MissingGuidFieldError(StandardAttributeError):
    """Raised when a missing name field is detected."""


class MissingRevisionFieldError(StandardAttributeError):
    """Raised when a missing name field is detected."""


class Parser2Interrupt(Exception):  # noqa: N818
    """Base class for implementing interrupts."""


class ExitParsingProcess2Interrupt(Exception):  # noqa: N818
    """Raised to stop parsing."""


class SkipTokenInterrupt(Exception):  # noqa: N818
    """Raised to skip all other actions that would be performed on current token."""
