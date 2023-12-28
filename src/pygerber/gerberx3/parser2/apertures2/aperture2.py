"""Parser level abstraction of aperture info for Gerber AST parser, version 2."""
from __future__ import annotations

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.common.immutable_map_model import ImmutableMapping


class Aperture2(FrozenGeneralModel):
    """Parser level abstraction of aperture info."""

    attributes: ImmutableMapping[str, str] = Field(default_factory=ImmutableMapping)

    def set_attribute(self, key: str, value: str) -> Aperture2:
        """Set aperture attribute."""
        return self.model_copy(
            update={
                "attributes": self.attributes.update(key, value),
            },
        )

    def get_attribute(self, key: str) -> str | None:
        """Get aperture attribute."""
        return self.attributes.get(key)
