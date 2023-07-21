"""Wrapper for aperture select token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic_core import CoreSchema, core_schema

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler
    from typing_extensions import Self


class DNNSelectAperture(Token):
    """Wrapper for aperture select token.

    Sets the current aperture to D code NN (NN ≥ 10).
    """

    aperture_identifier: ApertureID

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        aperture_identifier: ApertureID = tokens["aperture_identifier"]
        return cls(aperture_identifier=aperture_identifier)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"{self.aperture_identifier}*"


class ApertureID(str):
    """Aperture ID wrapper."""

    __slots__ = ()

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Generate the pydantic-core schema."""
        return core_schema.no_info_after_validator_function(cls, handler(str))
