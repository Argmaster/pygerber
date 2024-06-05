"""Class based on pydantic BaseModel with common set of features."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, computed_field


class FrozenGeneralModel(BaseModel):
    """Model with common set of general purpose features."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        arbitrary_types_allowed=True,
    )

    @computed_field  # type: ignore[misc]
    @property
    def __class_qualname__(self) -> str:
        """Name of class."""
        return self.__class__.__qualname__
