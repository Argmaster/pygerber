"""`pygerber.gerberx3.ast.errors` module gathers errors raised by visitors."""

from __future__ import annotations

from pygerber.gerberx3.ast.nodes.types import ApertureIdStr


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
