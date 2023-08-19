"""In-macro expression token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext


class Expression(Token):
    """Wrapper for in-macro expression."""

    def evaluate(
        self,
        macro_context: MacroContext,
        state: State,
        handle: PrivateApertureHandle,
        /,
    ) -> None:
        """Evaluate macro expression."""
