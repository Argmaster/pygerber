"""In-macro numeric expression token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext


class NumericExpression(Token):
    """Wrapper for in-macro numeric expression."""

    def evaluate_numeric(
        self,
        _macro_context: MacroContext,
        state: State,
        /,
    ) -> Offset:
        """Evaluate numeric value of this macro expression."""
        return Offset.new(value="0.0", unit=state.get_units())
