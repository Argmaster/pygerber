"""`model` module definition of common base class for all `VirtualMachine` related
model types.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, computed_field


class ModelType(BaseModel):
    """Common base class for all VM model types."""

    model_config = ConfigDict(
        extra="ignore",
        frozen=True,
        arbitrary_types_allowed=True,
    )

    @computed_field(repr=False)  # type: ignore[misc]
    @property
    def __class_qualname__(self) -> str:
        """Name of class."""
        return self.__class__.__qualname__
