"""Vector line macro primitive."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.parser2.macro2.primitives2.primitive2 import Primitive2

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Code2VectorLine2(Primitive2):
    """Vector line macro primitive."""

    def on_parser2_eval_statement(self, context: Parser2Context) -> None:
        """Evaluate macro to create concrete macro aperture."""
        context.hooks.macro_eval.on_code_2_vector_line(context, self)
