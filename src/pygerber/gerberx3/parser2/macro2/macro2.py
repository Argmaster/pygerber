"""Container for aperture macro elements."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.parser2.macro2.statement_buffer2 import ReadonlyStatementBuffer2

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class ApertureMacro2(FrozenGeneralModel):
    """Container for the elements contained within an aperture macro."""

    name: str
    statements: ReadonlyStatementBuffer2

    def on_parser2_eval_statement(self, context: Parser2Context) -> None:
        """Evaluate macro to create concrete macro aperture."""
        for stmt in self.statements:
            stmt.on_parser2_eval_statement(context)
