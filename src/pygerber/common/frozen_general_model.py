"""Class based on pydantic BaseModel with common set of features."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class FrozenGeneralModel(BaseModel):
    """Model with common set of general purpose features."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        arbitrary_types_allowed=True,
    )
