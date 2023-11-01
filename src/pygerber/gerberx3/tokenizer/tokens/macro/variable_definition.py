"""Macro variable definition token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext
from pygerber.gerberx3.tokenizer.tokens.macro.numeric_expression import (
    NumericExpression,
)
from pygerber.gerberx3.tokenizer.tokens.macro.variable_name import MacroVariableName

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self


class MacroVariableDefinition(Expression):
    """## 4.5.4.3 Definition of New Variable.

    New variables can be defined by an assign statement as follows: `$4=$1x1.25-$3`. The
    right-hand side is any arithmetic expression as in the previous section.

    The variable values are determined as follows:

    - `$1`, `$2`, ..., `$n` take the values of the n parameters of the calling AD command.
    - New variables get their value from their defining expression.
    - The undefined variables are 0.
    - Macro variables cannot be redefined.

    ---

    ## Example #1

    ```gerber
    %AMDONUTCAL*
    1,1,$1,$2,$3*
    $4=$1x1.25*
    1,0,$4,$2,$3*%
    ```

    The AD command contains four parameters which define the first four macro variables:

    ```yaml
    $1 = 0.02
    $2 = 0
    $3 = 0
    $4 = 0.06
    ```

    The variable `$5` is defined in the macro body and becomes

    ```yaml
    $5 = 0.06 x 0.25 = 0.015
    ```

    ## Example #2

    ```gerber
    %AMTEST1*
    1,1,$1,$2,$3*
    $4=$1x0.75*
    $5=($2+100)x1.75*
    1,0,$4,$5,$3*%
    ```

    ## Example #3

    ```
    %AMTEST2*
    $4=$1x0.75*
    $5=100+$3*
    1,1,$1,$2,$3*
    1,0,$4,$2,$5*
    $6=$4x0.5*
    1,0,$6,$2,$5*%
    ```

    ---

    See section 4.5.4.3 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=71)

    """  # noqa: E501

    def __init__(
        self,
        string: str,
        location: int,
        variable: MacroVariableName,
        value: NumericExpression,
    ) -> None:
        super().__init__(string, location)
        self.variable = variable
        self.value = value

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        variable = MacroVariableName.ensure_type(tokens["macro_variable_name"])
        value = NumericExpression.ensure_type(tokens["value"])
        return cls(
            string=string,
            location=location,
            variable=variable,
            value=value,
        )

    def evaluate(
        self,
        macro_context: MacroContext,
        state: State,
        handle: PrivateApertureHandle,
    ) -> None:
        """Evaluate macro expression."""
        name = self.variable.name
        value = self.value.evaluate_numeric(macro_context, state)
        macro_context.variables[name] = value

        return super().evaluate(macro_context, state, handle)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        return (
            f"{indent}{self.variable.get_gerber_code(endline=endline)}="
            f"{self.value.get_gerber_code(endline=endline)}"
        )

    def __str__(self) -> str:
        return f"{super().__str__()}::[{self.variable} = {self.value}]"
