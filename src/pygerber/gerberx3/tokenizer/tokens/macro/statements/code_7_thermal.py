"""Macro primitives tokens."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from pygerber.gerberx3.tokenizer.tokens.macro.expressions.macro_expression import (
    MacroExpressionToken,
)
from pygerber.gerberx3.tokenizer.tokens.macro.statements.primitive import (
    MacroPrimitiveToken,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Code7ThermalToken(MacroPrimitiveToken):
    """## 4.5.1.8 Thermal, Code 7.

    The thermal primitive is a ring (annulus) interrupted by four gaps. Exposure is
    always on.

    ---

    ## Example

    ```gerber
    %AMThermal*
    7,0,0,0.95,0.75,0.175,0.0*%
    ```

    ---

    See section 4.5.1.8 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=66)

    """

    symbol: ClassVar[str] = "7"

    def __init__(  # noqa: PLR0913
        self,
        string: str,
        location: int,
        center_x: MacroExpressionToken,
        center_y: MacroExpressionToken,
        outer_diameter: MacroExpressionToken,
        inner_diameter: MacroExpressionToken,
        gap: MacroExpressionToken,
        rotation: MacroExpressionToken,
    ) -> None:
        super().__init__(string, location)
        self.center_x = center_x
        self.center_y = center_y
        self.outer_diameter = outer_diameter
        self.inner_diameter = inner_diameter
        self.gap = gap
        self.rotation = rotation

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Initialize token object."""
        center_x = MacroExpressionToken.ensure_type(tokens["center_x"])
        center_y = MacroExpressionToken.ensure_type(tokens["center_y"])
        outer_diameter = MacroExpressionToken.ensure_type(tokens["outer_diameter"])
        inner_diameter = MacroExpressionToken.ensure_type(tokens["inner_diameter"])
        gap = MacroExpressionToken.ensure_type(tokens["gap"])
        rotation = MacroExpressionToken.ensure_type(tokens["rotation"])

        return cls(
            string,
            location,
            center_x=center_x,
            center_y=center_y,
            outer_diameter=outer_diameter,
            inner_diameter=inner_diameter,
            gap=gap,
            rotation=rotation,
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().macro_code_7_thermal.pre_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_7_thermal.on_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_7_thermal.post_parser_visit_token(
            self,
            context,
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        string = self.symbol

        string += f",{self.center_x.get_gerber_code(indent, endline)}"
        string += f",{self.center_y.get_gerber_code(indent, endline)}"
        string += f",{self.outer_diameter.get_gerber_code(indent, endline)}"
        string += f",{self.inner_diameter.get_gerber_code(indent, endline)}"
        string += f",{self.gap.get_gerber_code(indent, endline)}"
        string += f",{self.rotation.get_gerber_code(indent, endline)}"

        return indent + string

    def __str__(self) -> str:
        string = super().__str__()

        string += f"\n  {self.center_x}"
        string += f"\n  {self.center_y}"
        string += f"\n  {self.outer_diameter}"
        string += f"\n  {self.inner_diameter}"
        string += f"\n  {self.gap}"
        string += f"\n  {self.rotation}"

        return string
