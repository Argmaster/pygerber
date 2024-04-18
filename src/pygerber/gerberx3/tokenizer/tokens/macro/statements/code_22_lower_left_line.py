"""Code 22 lower left line macro primitive."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.macro.statements.primitive import (
    MacroPrimitiveToken,
)

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Code22LowerLeftLineToken(MacroPrimitiveToken):
    """Code 22 lower left line macro primitive."""

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().macro_code_22_lower_left_line.pre_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_22_lower_left_line.on_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_22_lower_left_line.post_parser_visit_token(
            self,
            context,
        )
