"""Defines a class used to identify aperture objects created by parser."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic_core import CoreSchema, core_schema

from pygerber.gerberx3.tokenizer.tokens.bases.gerber_code import GerberCode

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler


class ApertureID(str, GerberCode):
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

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{self}"
