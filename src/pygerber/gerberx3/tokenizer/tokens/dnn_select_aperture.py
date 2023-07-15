"""Wrapper for aperture select token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class DNNSelectAperture(Token):
    """Wrapper for aperture select token.

    Sets the current aperture to D code NN (NN ≥ 10).
    """

    aperture_identifier: str

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        aperture_identifier: str = tokens["aperture_identifier"]
        return cls(aperture_identifier=aperture_identifier)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"{self.aperture_identifier}*"
