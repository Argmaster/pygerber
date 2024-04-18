"""Macro primitive Moire."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.macro.statements.primitive import (
    MacroPrimitiveToken,
)

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Code6MoireToken(MacroPrimitiveToken):
    """Moire macro primitive."""

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().macro_code_6_moire.pre_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_6_moire.on_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_6_moire.post_parser_visit_token(
            self,
            context,
        )
