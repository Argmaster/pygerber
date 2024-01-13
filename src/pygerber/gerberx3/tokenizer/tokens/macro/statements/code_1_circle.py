"""Macro primitives tokens."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, ClassVar, Optional

from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokens.macro.expressions.macro_expression import (
    MacroExpressionToken,
)
from pygerber.gerberx3.tokenizer.tokens.macro.expressions.numeric_constant import (
    NumericConstant,
)
from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext
from pygerber.gerberx3.tokenizer.tokens.macro.statements.primitive import (
    MacroPrimitiveToken,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Code1CircleToken(MacroPrimitiveToken):
    """## 4.5.1.3 Circle, Code 1.

    A circle primitive is defined by its center point and diameter.

    ---

    ## Example

    ```gerber
    %AMCircle*
    1,1,1.5,0,0,0*%
    ```

    ---

    See section 4.5.1.3 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=60)

    """

    symbol: ClassVar[str] = "1"

    def __init__(
        self,
        string: str,
        location: int,
        exposure: MacroExpressionToken,
        diameter: MacroExpressionToken,
        center_x: MacroExpressionToken,
        center_y: MacroExpressionToken,
        rotation: MacroExpressionToken,
    ) -> None:
        super().__init__(string, location)
        self.exposure = exposure
        self.diameter = diameter
        self.center_x = center_x
        self.center_y = center_y
        self.rotation = rotation

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        exposure = MacroExpressionToken.ensure_type(tokens["exposure"])
        diameter = MacroExpressionToken.ensure_type(tokens["diameter"])
        center_x = MacroExpressionToken.ensure_type(tokens["center_x"])
        center_y = MacroExpressionToken.ensure_type(tokens["center_y"])

        r = tokens.get("rotation")
        rotation: Optional[MacroExpressionToken] = (
            MacroExpressionToken.ensure_type(r) if r is not None else None
        )
        if rotation is None:
            rotation = NumericConstant(string, location, value=Decimal("0.0"))

        return cls(
            string=string,
            location=location,
            exposure=exposure,
            diameter=diameter,
            center_x=center_x,
            center_y=center_y,
            rotation=rotation,
        )

    def evaluate(
        self,
        macro_context: MacroContext,
        state: State,
        handle: PrivateApertureHandle,
    ) -> None:
        """Evaluate macro expression."""
        self.exposure.evaluate_numeric(macro_context, state)
        self.diameter.evaluate_numeric(macro_context, state)
        self.center_x.evaluate_numeric(macro_context, state)
        self.center_y.evaluate_numeric(macro_context, state)
        self.rotation.evaluate_numeric(macro_context, state)

        return super().evaluate(macro_context, state, handle)

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().macro_code_1_circle.pre_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_1_circle.on_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_1_circle.post_parser_visit_token(
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

        string += f",{self.exposure.get_gerber_code(indent, endline)}"
        string += f",{self.diameter.get_gerber_code(indent, endline)}"
        string += f",{self.center_x.get_gerber_code(indent, endline)}"
        string += f",{self.center_y.get_gerber_code(indent, endline)}"

        if self.rotation is not None:
            string += f",{self.rotation.get_gerber_code(indent, endline)}"

        return indent + string

    def __str__(self) -> str:
        string = super().__str__()

        string += f"\n  {self.exposure}"
        string += f"\n  {self.diameter}"
        string += f"\n  {self.center_x}"
        string += f"\n  {self.center_y}"

        if self.rotation is not None:
            string += f"\n  {self.rotation}"

        return string
