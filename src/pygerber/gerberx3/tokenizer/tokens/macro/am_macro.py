"""Container token for macro definition."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, List, Tuple

from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext
from pygerber.gerberx3.tokenizer.tokens.token import Token
from pygerber.sequence_tools import flatten, unwrap

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class MacroDefinition(Token):
    """Container token for macro definition."""

    def __init__(
        self,
        string: str,
        location: int,
        macro_name: str,
        macro_body: List[Expression],
    ) -> None:
        super().__init__(string, location)
        self.macro_name = macro_name
        self.macro_body = macro_body

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        macro_name: str = str(tokens["macro_name"])
        macro_body: List[Expression] = [
            unwrap(e) for e in flatten(tokens["macro_body"])
        ]

        return cls(
            string=string,
            location=location,
            macro_name=macro_name,
            macro_body=macro_body,
        )

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Exit drawing process."""
        new_macros_dict = {**state.macros}
        new_macros_dict[self.macro_name] = self

        return (
            state.model_copy(
                update={
                    "macros": new_macros_dict,
                },
            ),
            (),
        )

    def evaluate(
        self,
        state: State,
        handle: PrivateApertureHandle,
        parameters: dict[str, Offset],
    ) -> None:
        """Evaluate macro into series of DrawCommands."""
        context = MacroContext()
        context.variables.update(parameters)

        for expression in self.macro_body:
            expression.evaluate(context, state, handle)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        body = endline.join(e.get_gerber_code(indent * 2) for e in self.macro_body)
        return f"AM{self.macro_name}*\n{body}\n"

    def __str__(self) -> str:
        lf = "\n"
        return (
            f"{super().__str__()}::[{self.macro_name}, "
            f"{lf.join(str(e) for e in self.macro_body)}]"
        )
