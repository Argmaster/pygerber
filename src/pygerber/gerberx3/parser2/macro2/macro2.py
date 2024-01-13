"""Container for aperture macro elements."""
from __future__ import annotations

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.parser2.macro2.statement_buffer2 import ReadonlyStatementBuffer2


class ApertureMacro2(FrozenGeneralModel):
    """Container for the elements contained within an aperture macro."""

    name: str
    statements: ReadonlyStatementBuffer2
