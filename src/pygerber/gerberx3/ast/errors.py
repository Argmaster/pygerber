"""`pygerber.gerberx3.ast.errors` module gathers errors raised by visitors."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.nodes import TF_MD5
    from pygerber.gerberx3.ast.nodes.types import ApertureIdStr


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
