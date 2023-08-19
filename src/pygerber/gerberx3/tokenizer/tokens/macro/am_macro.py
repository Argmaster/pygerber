"""Container token for macro definition."""

from __future__ import annotations

from textwrap import indent
from typing import TYPE_CHECKING, Any, Iterable, List, Tuple

from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext
from pygerber.gerberx3.tokenizer.tokens.token import Token
from pygerber.sequence_tools import flatten, unwrap

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class MacroDefinition(Token):
    """Container token for macro definition."""

    macro_name: str
    macro_body: List[Expression]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        macro_name: str = tokens["macro_name"]
        macro_body: List[Expression] = [
            unwrap(e) for e in flatten(tokens["macro_body"])
        ]

        return cls(macro_name=macro_name, macro_body=macro_body)

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

    def __str__(self) -> str:
        str_body = "\n".join(str(e) for e in self.macro_body)
        indented_body = indent(str_body, prefix="  ")
        return f"%AM{self.macro_name}*\n{indented_body}\n%"
