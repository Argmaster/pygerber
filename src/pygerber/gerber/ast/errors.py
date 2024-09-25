"""The `errors` module contains errors raised by visitor classes."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygerber.gerber.ast.nodes import TF_MD5
    from pygerber.gerber.ast.nodes.types import ApertureIdStr


class AstError(Exception):
    """Base class for all errors raised by AST."""


class VisitorError(Exception):
    """Base class for all errors raised by visitors."""


class StateTrackingVisitorError(VisitorError):
    """Base class for all errors raised by state tracking visitors."""


class DirectADHandlerDispatchNotSupportedError(StateTrackingVisitorError):
    """Raised when generic AD class is used to select aperture handler."""

    def __init__(self) -> None:
        super().__init__(
            "Aperture was not selected before flash command was issued."
            " PyGerber does not support direct use of AD class as handler."
        )


class ApertureNotSelectedError(StateTrackingVisitorError):
    """Raised when an aperture is not selected in the state tracking visitor."""

    def __init__(self) -> None:
        super().__init__(
            "Aperture was not selected before attempt was made to use it to draw."
        )


class ApertureNotFoundError(VisitorError):
    """Raised when an aperture is not found in the aperture dictionary."""

    def __init__(self, aperture_number: ApertureIdStr) -> None:
        self.aperture_number = aperture_number
        super().__init__(
            f"Aperture {aperture_number} not found in the aperture dictionary."
        )


class SourceNotAvailableError(AstError):
    """Raised when source is not available for MD5 check."""

    def __init__(self, node: TF_MD5) -> None:
        super().__init__("Source is not available for MD5 check.")
        self.node = node


class CoordinateFormatNotSetError(AstError):
    """Raised when coordinate parsing is requested but format was not prior to it."""


class PackedCoordinateTooLongError(AstError):
    """Raised when packed coordinate is too long for the format."""

    def __init__(self, coordinate: str, integer: int, decimal: int) -> None:
        self.coordinate = coordinate
        self.integer = integer
        self.decimal = decimal
        super().__init__(
            f"Packed coordinate {coordinate!r} is too long for the format"
            f"({integer},{decimal})."
        )


class PackedCoordinateTooShortError(AstError):
    """Raised when packed coordinate is too short for the format."""

    def __init__(self, coordinate: str, integer: int, decimal: int) -> None:
        self.coordinate = coordinate
        self.integer = integer
        self.decimal = decimal
        super().__init__(
            f"Packed coordinate {coordinate!r} is too short for the format "
            f"({integer},{decimal})."
        )
