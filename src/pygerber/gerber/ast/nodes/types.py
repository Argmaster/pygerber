"""Basic types for AST nodes."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic_core import CoreSchema, core_schema

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler
    from typing_extensions import TypeAlias

Double: TypeAlias = float
Integer: TypeAlias = int


class ApertureIdStr(str):
    """String subclass representing aperture ID."""

    __slots__ = ()

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))


class PackedCoordinateStr(str):
    """String subclass representing packed coordinates."""

    __slots__ = ()

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))
