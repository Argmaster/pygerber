"""Wrapper for aperture select token."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.token import Token


class BlockApertureBegin(Token):
    """Wrapper for AB begin token.

    Opens a block aperture statement and assigns its aperture number.
    """

    def __init__(self, aperture_identifier: str) -> None:
        """Initialize token object."""
        super().__init__()
        self.aperture_identifier = aperture_identifier

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"AB{self.aperture_identifier}*"


class BlockApertureEnd(Token):
    """Wrapper for AB end token.

    Ends block aperture statement.
    """

    def __init__(self) -> None:
        """Initialize token object."""
        super().__init__()

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return "AB*"
