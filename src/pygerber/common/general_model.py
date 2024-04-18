"""Class based on pydantic BaseModel with common set of features."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class GeneralModel(BaseModel):
    """Model with common set of general purpose features."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=False,
        arbitrary_types_allowed=True,
    )
