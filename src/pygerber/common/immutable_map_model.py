"""Module contains model class wrapping immutable mapping."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, Dict, Generic, Mapping, Optional, TypeVar

from pydantic import Field, FieldSerializationInfo, field_serializer, field_validator

from pygerber.common.frozen_general_model import FrozenGeneralModel

if TYPE_CHECKING:
    from typing_extensions import Self

KeyT = TypeVar("KeyT")
ValueT = TypeVar("ValueT")


class ImmutableMapping(FrozenGeneralModel, Generic[KeyT, ValueT]):
    """Model class wrapping immutable dictionary."""

    mapping: Mapping[KeyT, ValueT] = Field(
        default_factory=lambda: MappingProxyType({}),
    )

    @field_validator("mapping")
    @classmethod
    def _validate_mapping(cls, v: Mapping[str, str]) -> Mapping[str, str]:
        if isinstance(v, MappingProxyType):
            return v
        if isinstance(v, dict):
            return MappingProxyType(v)
        raise TypeError(type(v))

    @field_serializer("mapping", return_type=Dict[KeyT, ValueT])
    def _serialize_mapping(
        self,
        mapping: Mapping[KeyT, ValueT],
        _info: FieldSerializationInfo,
    ) -> Dict[KeyT, ValueT]:
        """Serialize model instance."""
        return dict(mapping)

    def update(self, __key: KeyT, __value: ValueT) -> Self:
        """Update underlying mapping."""
        return self.model_copy(
            update={
                "mapping": MappingProxyType(
                    {
                        **self.mapping,
                        __key: __value,
                    },
                ),
            },
        )

    def get(self, __key: KeyT, __default: Optional[ValueT] = None) -> Optional[ValueT]:
        """Get item if exists or add it to mapping with __default value and return."""
        return self.mapping.get(__key, __default)

    def delete(self, __key: KeyT) -> Self:
        """Remove entry from mapping."""
        return self.model_copy(
            update={
                "mapping": MappingProxyType(
                    {k: v for k, v in self.mapping.items() if (k != __key)},
                ),
            },
        )
