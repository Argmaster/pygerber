"""In-macro numeric expression token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.tokenizer.tokens.bases.token import Token

if TYPE_CHECKING:
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context
    from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2
    from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext


class MacroExpressionToken(Token):
    """## 4.5.4.2 Arithmetic Expressions.

    A parameter value can also be defined by an arithmetic expression consisting of integer and
    decimal constants, other variables, arithmetic operators and the brackets "(" and ")". The
    standard arithmetic precedence rules apply. The following arithmetic operators are available:

    ---

    ## Example

    ```gerber
    %AMRect*
    21,1,$1,$2-2x$3,-$4,-$5+$2,0*%
    ```

    The corresponding AD command could be:

    ```gerber
    %ADD146Rect,0.0807087X0.1023622X0.0118110X0.5000000X0.3000000*%
    ```

    ---

    See section 4.5.4.2 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=70)

    """  # noqa: E501

    def to_parser2_expression(self, context: Parser2Context) -> Expression2:
        """Convert to `Expression2` descendant class."""
        raise NotImplementedError

    def evaluate_numeric(
        self,
        _macro_context: MacroContext,
        state: State,
        /,
    ) -> Offset:
        """Evaluate numeric value of this macro expression."""
        return Offset.new(value="0.0", unit=state.get_units())
