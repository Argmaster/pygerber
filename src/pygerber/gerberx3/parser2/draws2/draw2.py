"""Parser level abstraction of draw operation for Gerber AST parser, version 2."""
from __future__ import annotations

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.common.immutable_map_model import ImmutableMapping


class Draw2(FrozenGeneralModel):
    """Parser level abstraction of draw operation for Gerber AST parser, version 2."""

    attributes: ImmutableMapping = Field(default_factory=ImmutableMapping)
