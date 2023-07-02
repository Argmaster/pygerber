"""Wrapper for aperture select token."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.token import Token


class BeginRegion(Token):
    """Wrapper for G36 token.

    Starts a region statement which creates a region by defining its contours.
    """

    def __init__(self) -> None:
        """Initialize token object."""
        super().__init__()

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return "G36*"


class EndRegion(Token):
    """Wrapper for G37 token.

    Ends the region statement.
    """

    def __init__(self) -> None:
        """Initialize token object."""
        super().__init__()

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return "G37*"
