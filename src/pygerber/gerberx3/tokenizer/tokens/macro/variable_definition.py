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
    """Wrapper for macro variable definition."""

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
            f"{self.value.get_gerber_code(endline=endline)}*"
        )

    def __str__(self) -> str:
        return f"{super().__str__()}::[{self.variable} = {self.value}]"
