"""Wrapper for aperture select token."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.token import Token


class DNNSelectAperture(Token):
    """Wrapper for aperture select token.

    Sets the current aperture to D code NN (NN ≥ 10).
    """

    def __init__(self, aperture_identifier: str) -> None:
        """Initialize token object."""
        super().__init__()
        self.aperture_identifier = aperture_identifier

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"{self.aperture_identifier}*"
