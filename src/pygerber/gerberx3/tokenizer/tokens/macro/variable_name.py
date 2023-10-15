"""Macro variable use token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext
from pygerber.gerberx3.tokenizer.tokens.macro.numeric_expression import (
    NumericExpression,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self


class MacroVariableName(NumericExpression):
    """## 4.5.4.1 Variable Values from the AD Command.

    description

    ---

    ## Example

    ```gerber
    %AMDONUTVAR*1,1,$1,$2,$3*1,0,$4,$2,$3*%
    ```
    `$1`, `$2`, `$3` and `$4` are macro variables. With the following calling AD.

    ```gerber
    %ADD34DONUTVAR,0.100X0X0X0.080*%
    ```

    the variables take the following values:

    ```yaml
    $1 = 0.100
    $2 = 0
    $3 = 0
    $4 = 0.080
    ```

    ---

    See section 4.5.4.1 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=70)

    """

    def __init__(self, string: str, location: int, name: str) -> None:
        super().__init__(string, location)
        self.name = name

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        name = str(tokens["macro_variable_name"])
        return cls(string=string, location=location, name=name)

    def evaluate_numeric(self, macro_context: MacroContext, _state: State) -> Offset:
        """Evaluate numeric value of this macro expression."""
        return macro_context.variables[self.name]

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return self.name
